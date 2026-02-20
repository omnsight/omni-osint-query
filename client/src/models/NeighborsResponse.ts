/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Event } from './Event';
import type { Organization } from './Organization';
import type { Person } from './Person';
import type { Relation } from './Relation';
import type { Source } from './Source';
import type { Website } from './Website';
export type NeighborsResponse = {
    events?: Array<Event>;
    sources?: Array<Source>;
    persons?: Array<Person>;
    organizations?: Array<Organization>;
    websites?: Array<Website>;
    relations?: Array<Relation>;
};

