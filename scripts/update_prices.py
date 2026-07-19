import json
import re
import sys
import time
import os
from DrissionPage import ChromiumPage, ChromiumOptions

JSON_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src/data/llm-plans.json')

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def run_crawler():
    print("Loading LLM plans JSON...")
    try:
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading {JSON_PATH}: {e}", file=sys.stderr)
        sys.exit(1)

    print("Configuring ChromiumOptions...")
    co = ChromiumOptions()
    # Use standard Chrome path on system
    chrome_path = '/usr/bin/google-chrome'
    if os.path.exists(chrome_path):
        co.set_browser_path(chrome_path)
    
    co.set_local_port(9333)
    co.set_user_data_path(os.path.join(os.path.dirname(__file__), 'chrome_data'))
    co.headless(True)
    
    # Linux sandbox flags
    co.set_argument('--no-sandbox')
    co.set_argument('--disable-gpu')
    co.set_argument('--disable-dev-shm-usage')
    co.set_argument('--disable-setuid-sandbox')
    co.set_argument('--remote-allow-origins=*')

    try:
        print("Launching ChromiumPage...")
        page = ChromiumPage(co)
    except Exception as e:
        print(f"Failed to start headless browser: {e}", file=sys.stderr)
        print("Falling back. No prices will be updated.", file=sys.stderr)
        sys.exit(1)

    updated_count = 0
    warnings = []

    try:
        # 1. Fetch DeepSeek Domestic Prices (Chinese Page)
        deepseek_cn_input = None
        deepseek_cn_output = None
        deepseek_flash_cn_input = None
        deepseek_flash_cn_output = None
        
        print("\n[DeepSeek CN] Scraping domestic prices...")
        try:
            page.get('https://api-docs.deepseek.com/zh-cn/quick_start/pricing/')
            page.wait.load_start()
            time.sleep(3)
            body_text = page.ele('tag:body').text
            
            for line in body_text.split('\n'):
                parts = [p.strip() for p in re.split(r'\t|\s{2,}', line) if p.strip()]
                if not parts:
                    continue
                
                if any('缓存未命中' in p for p in parts):
                    nums = []
                    for p in parts[1:]:
                        m = re.search(r'([\d.]+)', p)
                        if m:
                            nums.append(float(m.group(1)))
                    if len(nums) >= 2:
                        deepseek_flash_cn_input = nums[0]
                        deepseek_cn_input = nums[1]
                        
                elif any('百万tokens输出' in p for p in parts) and not any('输入' in p for p in parts):
                    nums = []
                    for p in parts[1:]:
                        m = re.search(r'([\d.]+)', p)
                        if m:
                            nums.append(float(m.group(1)))
                    if len(nums) >= 2:
                        deepseek_flash_cn_output = nums[0]
                        deepseek_cn_output = nums[1]
            
            print(f"[DeepSeek CN] Flash: Input={deepseek_flash_cn_input}元, Output={deepseek_flash_cn_output}元")
            print(f"[DeepSeek CN] Pro: Input={deepseek_cn_input}元, Output={deepseek_cn_output}元")
        except Exception as e:
            print(f"[DeepSeek CN] Scrape failed: {e}", file=sys.stderr)
            warnings.append(f"DeepSeek Domestic pricing page scrape failed: {e}")

        # 2. Fetch DeepSeek International Prices (English Page)
        deepseek_intl_input = None
        deepseek_intl_output = None
        
        print("\n[DeepSeek Intl] Scraping international prices...")
        try:
            page.get('https://api-docs.deepseek.com/quick_start/pricing/')
            page.wait.load_start()
            time.sleep(3)
            body_text = page.ele('tag:body').text
            
            for line in body_text.split('\n'):
                parts = [p.strip() for p in re.split(r'\t|\s{2,}', line) if p.strip()]
                if not parts:
                    continue
                
                if any('CACHE MISS' in p.upper() for p in parts):
                    nums = []
                    for p in parts[1:]:
                        m = re.search(r'([\d.]+)', p)
                        if m:
                            nums.append(float(m.group(1)))
                    if len(nums) >= 2:
                        # Index 1 is deepseek-v4-pro
                        deepseek_intl_input = nums[1]
                        
                elif any('OUTPUT TOKENS' in p.upper() for p in parts):
                    nums = []
                    for p in parts[1:]:
                        m = re.search(r'([\d.]+)', p)
                        if m:
                            nums.append(float(m.group(1)))
                    if len(nums) >= 2:
                        deepseek_intl_output = nums[1]
            
            print(f"[DeepSeek Intl] Pro: Input=${deepseek_intl_input}, Output=${deepseek_intl_output}")
        except Exception as e:
            print(f"[DeepSeek Intl] Scrape failed: {e}", file=sys.stderr)
            warnings.append(f"DeepSeek International pricing page scrape failed: {e}")

        # 3. Fetch GLM (智谱AI) Prices
        glm_input = None
        glm_output = None
        
        print("\n[GLM] Scraping GLM prices...")
        try:
            page.get('https://bigmodel.cn/pricing')
            page.wait.load_start()
            time.sleep(3)
            body_text = page.ele('tag:body').text
            
            lines = body_text.split('\n')
            for idx, line in enumerate(lines):
                if line.strip() == 'GLM-5.2':
                    prices = []
                    for sub_line in lines[idx+1:idx+10]:
                        sub_line_clean = sub_line.strip()
                        if '元' in sub_line_clean:
                            m = re.search(r'([\d.]+)\s*元', sub_line_clean)
                            if m:
                                prices.append(float(m.group(1)))
                    if len(prices) >= 2:
                        glm_input = prices[0]
                        glm_output = prices[1]
                    break
            
            print(f"[GLM] GLM-5.2: Input={glm_input}元, Output={glm_output}元")
        except Exception as e:
            print(f"[GLM] Scrape failed: {e}", file=sys.stderr)
            warnings.append(f"GLM pricing page scrape failed: {e}")

        # Process the updates in our JSON data structure
        for company in data:
            comp_name = company.get('name')
            for plan in company.get('plans', []):
                plan_name = plan.get('name')
                curr_price = plan.get('price')
                url = plan.get('url')
                
                # Apply extraction logic
                if comp_name == "DeepSeek (深度求索)":
                    if plan_name == "API (V4-Pro, 国内)" and deepseek_cn_input and deepseek_cn_output:
                        new_price = f"输入 ¥{deepseek_cn_input:g}/百万tokens，输出 ¥{deepseek_cn_output:g}/百万tokens"
                        if curr_price != new_price:
                            print(f"[UPDATE] {comp_name} - {plan_name}: '{curr_price}' -> '{new_price}'")
                            plan['price'] = new_price
                            updated_count += 1
                        else:
                            print(f"[NO CHANGE] {comp_name} - {plan_name}: '{curr_price}'")
                    elif plan_name == "API (V4-Flash" and deepseek_flash_cn_input and deepseek_flash_cn_output:
                        # Note: the key in the original json is "API (V4-Flash" (missing closing paren)
                        new_price = f"输入 ¥{deepseek_flash_cn_input:g}/MTok, 输出 ¥{deepseek_flash_cn_output:g}/MTok"
                        if curr_price != new_price:
                            print(f"[UPDATE] {comp_name} - {plan_name}: '{curr_price}' -> '{new_price}'")
                            plan['price'] = new_price
                            updated_count += 1
                        else:
                            print(f"[NO CHANGE] {comp_name} - {plan_name}: '{curr_price}'")
                    elif plan_name == "API (V4-Pro, International)" and deepseek_intl_input and deepseek_intl_output:
                        new_price = f"Input ${deepseek_intl_input:g}/MTok, Output ${deepseek_intl_output:g}/MTok"
                        if curr_price != new_price:
                            print(f"[UPDATE] {comp_name} - {plan_name}: '{curr_price}' -> '{new_price}'")
                            plan['price'] = new_price
                            updated_count += 1
                        else:
                            print(f"[NO CHANGE] {comp_name} - {plan_name}: '{curr_price}'")
                    else:
                        if plan_name in ["API (V4-Pro, 国内)", "API (V4-Flash", "API (V4-Pro, International)"]:
                            warnings.append(f"Could not extract price for '{comp_name}' - '{plan_name}'. Keeping current value: '{curr_price}'")
                
                elif comp_name == "智谱AI (GLM)":
                    if plan_name == "API (GLM-5.2)" and glm_input and glm_output:
                        new_price = f"输入 ¥{glm_input:g}/MTok, 输出 ¥{glm_output:g}/MTok"
                        if curr_price != new_price:
                            print(f"[UPDATE] {comp_name} - {plan_name}: '{curr_price}' -> '{new_price}'")
                            plan['price'] = new_price
                            updated_count += 1
                        else:
                            print(f"[NO CHANGE] {comp_name} - {plan_name}: '{curr_price}'")
                    elif plan_name == "API (GLM-5.2)":
                        warnings.append(f"Could not extract price for '{comp_name}' - '{plan_name}'. Keeping current value: '{curr_price}'")
                    else:
                        # Other plans under GLM (like Free, Coding plans) are not auto-scraped.
                        # Report keep current price.
                        warnings.append(f"Auto-scraping not configured for '{comp_name}' - '{plan_name}'. Keeping current value: '{curr_price}'")
                
                else:
                    # Generic fallback warnings for all other plans
                    warnings.append(f"Auto-scraping not configured for '{comp_name}' - '{plan_name}' (URL: {url}). Keeping current value: '{curr_price}'")

    finally:
        page.quit()

    # Save data if updated
    if updated_count > 0:
        print(f"\nWriting {updated_count} updates back to {JSON_PATH}...")
        try:
            with open(JSON_PATH, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print("Successfully updated JSON file.")
        except Exception as e:
            print(f"Error writing to {JSON_PATH}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("\nNo price changes detected or all scrapers failed. JSON file remains unchanged.")

    # Print friendly warnings for not scraped or failed links
    if warnings:
        print("\n" + "="*30 + " FRIENDLY SCRAPING NOTICES " + "="*30)
        for warn in warnings:
            print(f"[NOTICE] {warn}")
        print("="*87)

if __name__ == "__main__":
    run_crawler()
