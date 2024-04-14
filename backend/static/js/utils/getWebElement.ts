export function getWebElement<K extends keyof HTMLElementTagNameMap>(
    tagName: K,
    className?: string,
    content?: string
): HTMLElementTagNameMap[K] {
    const webElement = document.createElement(tagName);
    className && webElement.setAttribute('class', className);
    content && (webElement.textContent = content);
    return webElement;
}
