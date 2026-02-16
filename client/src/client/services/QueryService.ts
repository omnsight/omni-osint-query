/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { NeighborsRequest } from '../models/NeighborsRequest';
import type { NeighborsResponse } from '../models/NeighborsResponse';
import type { QueryRequest } from '../models/QueryRequest';
import type { QueryResponse } from '../models/QueryResponse';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class QueryService {

    /**
     * Execute Query
     * @param requestBody
     * @param authorization
     * @returns QueryResponse Successful Response
     * @throws ApiError
     */
    public static executeQueryQueryQueryEventsPost(
        requestBody: QueryRequest,
        authorization?: (string | null),
    ): CancelablePromise<QueryResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/query/query_events',
            headers: {
                'authorization': authorization,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Neighbors
     * @param requestBody
     * @param authorization
     * @returns NeighborsResponse Successful Response
     * @throws ApiError
     */
    public static getNeighborsQueryNeighborsPost(
        requestBody: NeighborsRequest,
        authorization?: (string | null),
    ): CancelablePromise<NeighborsResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/query/neighbors',
            headers: {
                'authorization': authorization,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
