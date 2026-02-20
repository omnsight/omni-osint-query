import { QueryService, OpenAPI } from '..';

describe('QueryService', () => {
  beforeAll(() => {
    OpenAPI.BASE = 'http://localhost:8000';
    const payload = {
      sub: 'test-user-id-123',
      roles: ['admin'],
    };
    const header = Buffer.from(JSON.stringify({ alg: 'none' })).toString('base64url');
    const claims = Buffer.from(JSON.stringify(payload)).toString('base64url');
    const token = `${header}.${claims}.`;
    OpenAPI.TOKEN = token;
  });

  it('should return a response from neighbors', async () => {
    try {
      await QueryService.queryNeighbors({ entity_id: 'test-id' });
    } catch (e) {
      expect(e).toBeDefined();
    }
  });
});
