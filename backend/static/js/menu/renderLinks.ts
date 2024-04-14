import { getWebElement } from '../utils/getWebElement.js';

type TLink = {
    id: number;
    name: string;
    href: string;
    parent: TLink | null;
    childs: TLink[];
};

export function renderLinks(links: TLink[], target: HTMLElement) {
    links.forEach((link) => {
        const LinkGroup = getWebElement('ul', 'LinkGroup', '');
        const Link = getWebElement('li', 'Link', '');
        const LinkText = getWebElement('a', 'LinkText', '');
        const LinkToggler = getWebElement('button', 'LinkToggler', '+');

        const RootTo = target.querySelector('.LinkText')?.getAttribute('href');
        const href = RootTo ? `${RootTo}${link.href}/` : `${link.href}/`;
        LinkText.setAttribute('href', href);
        LinkText.textContent = link.name;
        Link.appendChild(LinkText);

        if (link.childs.length !== 0) {
            LinkToggler.addEventListener('click', (event) => handleClick(event, link));
            Link.appendChild(LinkToggler);
        }

        LinkGroup.appendChild(Link);
        target.appendChild(LinkGroup);
    });
}

function handleClick(event: MouseEvent, link) {
    const toggler = event.target as HTMLButtonElement;
    const linkRow = toggler.parentElement as HTMLLIElement;
    const linkGroup = linkRow.parentElement as HTMLUListElement;

    const isOpen = linkGroup.hasAttribute('data-open');
    linkGroup.toggleAttribute('data-open');

    if (isOpen) {
        toggler.innerText = '+';
        linkGroup.innerHTML = '';
        linkGroup.appendChild(linkRow);
    } else {
        toggler.innerText = '-';
        renderLinks(link.childs, linkGroup);
    }
}
