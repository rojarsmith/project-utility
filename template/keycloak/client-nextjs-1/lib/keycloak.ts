import Keycloak from 'keycloak-js';

let keycloak: Keycloak | null = null;

export function getKeycloak(): Keycloak {
  if (!keycloak) {
    keycloak = new Keycloak({
      url: 'https://keycloak.neuhex.com',
      realm: 'quick-start',
      clientId: 'quick-start',
    });
  }
  return keycloak;
}
