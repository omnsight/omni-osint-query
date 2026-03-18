/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Event } from './Event';
import type { Relation } from './Relation';
export type QueryResponse = {
    /**
     * A list of events that match the query.
     */
    events?: Array<Event>;
    /**
     * A list of relations that match the query.
     */
    relations?: Array<Relation>;
    /**
     * The offset from which to start returning results.
     */
    offset?: number;
};

