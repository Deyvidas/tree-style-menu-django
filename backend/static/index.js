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
        parent.innerHTML = '';
        parent.appendChild(target);
    } else {
        renderLinks(link.childrens, parent);
    }
}

function renderLinks(links, target) {
    links.forEach((link) => {
        const LinkGroup = getWebElement('ul', '', 'LinkGroup');
        const Link = getWebElement('li', '', 'Link');
        const LinkText = getWebElement('span', '', 'LinkText');
        const LinkToggler = getWebElement('button', '+', 'LinkToggler');

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
