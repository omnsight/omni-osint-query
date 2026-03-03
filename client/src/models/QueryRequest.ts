/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type QueryRequest = {
    /**
     * The search query string.
     */
    query?: (string | null);
    /**
     * The start of the date range for the query.
     */
    date_start?: (number | null);
    /**
     * The end of the date range for the query.
     */
    date_end?: (number | null);
    /**
     * The country code to filter the query by.
     */
    country_code?: (string | null);
    /**
     * The maximum number of results to return.
     */
    limit?: number;
    /**
     * The offset from which to start returning results.
     */
    offset?: number;
};

