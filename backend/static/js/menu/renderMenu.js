import { renderLinks } from './renderLinks.js';
export function renderMenu(menu, menuId) {
    var root = document.querySelector("#".concat(menuId));
    renderLinks([menu], root);
}
