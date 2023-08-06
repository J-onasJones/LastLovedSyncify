/**
 * @param {string} name
 * @param {string} value
 * @param {number} days
 */
export function setCookie(name, value, days) {
    const expires = new Date();
    expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
    document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
  }
  
/**
 * @param {string} name
 */
export function getCookie(name) {
  try {
    const value = "; " + document.cookie;
    const parts = value.split("; " + name + "=");
    if (parts.length === 2) return parts.pop().split(";").shift();
  } catch (e) {
    console.error(e);
    return null;
  }
}