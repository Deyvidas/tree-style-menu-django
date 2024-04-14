export function getWebElement(tagName, className, content) {
    var webElement = document.createElement(tagName);
    className && webElement.setAttribute('class', className);
    content && (webElement.textContent = content);
    return webElement;
}
