import { client } from '../src/client.gen';
import { queryEvents } from '../src/sdk.gen';

describe('QueryEvents', () => {
  beforeAll(() => {
    const payload = {
      sub: 'test-user-id-123',
      roles: ['admin'],
    };
    const header = Buffer.from(JSON.stringify({ alg: 'none' })).toString('base64url');
    const claims = Buffer.from(JSON.stringify(payload)).toString('base64url');
    const token = `${header}.${claims}.`;

    client.setConfig({
      baseURL: "http://localhost:8000",
      withCredentials: true,
    });
    client.instance.interceptors.request.use((config) => {
      config.headers['Authorization'] = `Bearer ${token}`;
      return config;
    });
  });

  it('should return a health check', async () => {
    const {data, error, status} = await queryEvents({
      body: {
        query: "",
        date_start: Math.floor(Date.now() / 1000 - 60 * 60),
        date_end: Math.floor(Date.now() / 1000 + 60 * 60),
      }
    });
    console.log(data, error, status);
    expect(data).toBeDefined();
    expect(status).toEqual(200);
  });
});
