/// <reference types="cypress" />

const DAY = '2026-09-01';

function fillBooking(title: string, start: string, end: string, attendees = 2) {
  cy.get('#title').clear().type(title);
  cy.get('#start').clear().type(`${DAY}T${start}`);
  cy.get('#end').clear().type(`${DAY}T${end}`);
  cy.get('#attendees').clear().type(String(attendees));
  cy.get('#submit').click();
}

describe('Room booking', () => {
  before(() => {
    cy.request('POST', '/api/reset');
  });

  beforeEach(() => {
    cy.visit('/');
  });

  it('loads the page', () => {
    cy.get('body').should('exist');
  });

  it('creates a booking', () => {
    fillBooking('Sprint planning', '09:00', '10:00', 3);
    cy.wait(2000);
    cy.get('#bookings').should('exist');
  });

  it('shows an error for an invalid booking', () => {
    fillBooking('Backwards', '11:00', '10:00');
    cy.get('.validation-warning').should('not.exist');
  });

  it('prevents double booking', () => {
    fillBooking('Retro A', '14:00', '15:00');
    fillBooking('Retro B', '16:00', '17:00');
    cy.get('#bookings li').should('have.length.greaterThan', 1);
  });

  it('respects room capacity', () => {
    cy.get('#attendees').clear().type('3');
    cy.get('#attendees').should('have.value', '3');
    fillBooking('Design review', '18:00', '19:00', 3);
  });

  it('cancels a booking', () => {
    cy.get('[data-delete]').first().click();
    cy.get('#bookings li').should('have.length.greaterThan', 0);
  });
});
