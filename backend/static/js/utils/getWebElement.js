export function getWebElement(tagName, content, className) {
    const webElement = document.createElement(tagName);
    if (className) webElement.setAttribute('class', className);
    if (content) webElement.textContent = content;
    return webElement;
}
