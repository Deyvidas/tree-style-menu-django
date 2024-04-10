const Root = document.querySelector('#root');
const NavLinks = getWebElement('div', '', 'NavLinks');
Root.appendChild(NavLinks);

function getWebElement(tagName, content, className) {
    const webElement = document.createElement(tagName);
    if (className) webElement.setAttribute('class', className);
    if (content) webElement.textContent = content;
    return webElement;
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
        renderLinks(link.childrens, parent);
    }
}

function renderLinks(links, target) {
    links.forEach((link) => {
        const LinkGroup = getWebElement('ul', '', 'LinkGroup');
        const Link = getWebElement('li', '', 'Link');
        const LinkText = getWebElement('a', '', 'LinkText');
        const LinkToggler = getWebElement('button', '+', 'LinkToggler');

        const RootTo = target.querySelector('.LinkText')?.getAttribute('href');
        const href = RootTo ? `${RootTo}${link.to}/` : `${link.to}/`;
        LinkText.setAttribute('href', href);
        LinkText.textContent = link.name;
        Link.appendChild(LinkText);

        if (link.childrens.length !== 0) {
            LinkToggler.addEventListener('click', (event) => handleClick(event, link));
            Link.appendChild(LinkToggler);
        }

        LinkGroup.appendChild(Link);
        target.appendChild(LinkGroup);
    });
}

renderLinks(links, NavLinks);
