// Place any global data in this file.
// You can import this data from anywhere in your site by using the `import` keyword.

export const SITE_TITLE = 'Zhou Shouyu';
export const SITE_DESCRIPTION = 'The portfolio of Zhou Shouyu.';

export const CV_URL = '/cv.pdf';

export const CONTACT = {
  organization: 'Microcyclone',
  addressLines: [
    'Senior Software Engineer',
  ],
  emails: [
    'syzhou98@foxmail.com',
  ],
};

export type SocialIcon = 'website' | 'scholar' | 'email' | 'github' | 'linkedin' | 'twitter';

export const SOCIAL_LINKS: ReadonlyArray<{
  label: string;
  href: string;
  icon: SocialIcon;
}> = [
  {
    label: 'GitHub',
    href: 'https://github.com/cyclone/Shouyu-blog',
    icon: 'github',
  },
  {
    label: 'Email',
    href: 'mailto:syzhou98@foxmail.com',
    icon: 'email',
  },
  // {
  //   label: 'LinkedIn',
  //   href: 'https://www.linkedin.com/in/shravangoswami/',
  //   icon: 'linkedin',
  // },
  {
    label: 'X',
    href: 'https://x.com/Zhoushu9763',
    icon: 'twitter',
  },
];

export const FOOTER_CREDIT = {
  designerName: 'Shravan Goswami',
  designerUrl: 'https://shravangoswami.com',
  sourceLabel: 'Open Source',
  sourceUrl: 'https://github.com/shravanngoswamii/astro-scholar',
};
