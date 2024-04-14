import { getWebElement } from '../utils/index.js';

export function renderLinks(links, target) {
    links.forEach((link) => {
        const LinkGroup = getWebElement('ul', '', 'LinkGroup');
        const Link = getWebElement('li', '', 'Link');
        const LinkText = getWebElement('a', '', 'LinkText');
        const LinkToggler = getWebElement('button', '+', 'LinkToggler');

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

function handleClick(event, link) {
    const target = event.target.parentElement;
    const parent = target.parentElement;

    const isOpen = parent.hasAttribute('data-open');
    parent.toggleAttribute('data-open');

    if (isOpen) {
        event.target.innerText = '+';
        parent.innerHTML = '';
        parent.appendChild(target);
    } else {
        event.target.innerText = '-';
        renderLinks(link.childs, parent);
    }
}
