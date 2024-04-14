import { renderLinks } from './renderLinks.js';

export function renderMenu(menu, menuId) {
    const Root = document.querySelector(`#${menuId}`);
    renderLinks([menu], Root);
}
