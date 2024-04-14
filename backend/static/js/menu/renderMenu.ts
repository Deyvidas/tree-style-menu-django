import { renderLinks } from './renderLinks.js';

export function renderMenu(menu, menuId) {
    const root = document.querySelector(`#${menuId}`) as HTMLDivElement;
    renderLinks([menu], root);
}
