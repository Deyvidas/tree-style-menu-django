import { getWebElement } from '../utils/getWebElement.js';
export function renderLinks(links, target) {
    links.forEach(function (link) {
        var _a;
        var LinkGroup = getWebElement('ul', 'LinkGroup', '');
        var Link = getWebElement('li', 'Link', '');
        var LinkText = getWebElement('a', 'LinkText', '');
        var LinkToggler = getWebElement('button', 'LinkToggler', '+');
        var RootTo = (_a = target.querySelector('.LinkText')) === null || _a === void 0 ? void 0 : _a.getAttribute('href');
        var href = RootTo ? "".concat(RootTo).concat(link.href, "/") : "".concat(link.href, "/");
        LinkText.setAttribute('href', href);
        LinkText.textContent = link.name;
        Link.appendChild(LinkText);
        if (link.childs.length !== 0) {
            LinkToggler.addEventListener('click', function (event) { return handleClick(event, link); });
            Link.appendChild(LinkToggler);
        }
        LinkGroup.appendChild(Link);
        target.appendChild(LinkGroup);
    });
}
function handleClick(event, link) {
    var toggler = event.target;
    var linkRow = toggler.parentElement;
    var linkGroup = linkRow.parentElement;
    var isOpen = linkGroup.hasAttribute('data-open');
    linkGroup.toggleAttribute('data-open');
    if (isOpen) {
        toggler.innerText = '+';
        linkGroup.innerHTML = '';
        linkGroup.appendChild(linkRow);
    }
    else {
        toggler.innerText = '-';
        renderLinks(link.childs, linkGroup);
    }
}
