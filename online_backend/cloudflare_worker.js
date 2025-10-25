/**
 * KOF Ultimate Online - Cloudflare Worker
 * Worker pour exposer l'API backend via Cloudflare
 *
 * Déployer avec: wrangler publish
 */

// Configuration
const BACKEND_API_URL = 'YOUR_BACKEND_URL'; // À remplacer par votre URL backend (Cloudflare Tunnel)
const ALLOWED_ORIGINS = [
    'http://localhost',
    'https://kof-ultimate.pages.dev',
    // Ajoutez vos domaines
];

// CORS Headers
function corsHeaders(origin) {
    const allowedOrigin = ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0];

    return {
        'Access-Control-Allow-Origin': allowedOrigin,
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, PATCH, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Max-Age': '86400',
    };
}

// Handle CORS preflight
function handleOptions(request) {
    const origin = request.headers.get('Origin') || '';
    return new Response(null, {
        headers: corsHeaders(origin)
    });
}

// Proxy request to backend
async function proxyToBackend(request) {
    const url = new URL(request.url);
    const backendUrl = `${BACKEND_API_URL}${url.pathname}${url.search}`;

    const headers = new Headers(request.headers);
    headers.delete('host'); // Remove host header

    const init = {
        method: request.method,
        headers: headers,
    };

    // Add body for POST/PUT/PATCH
    if (request.method !== 'GET' && request.method !== 'HEAD') {
        init.body = await request.text();
    }

    try {
        const response = await fetch(backendUrl, init);
        const responseBody = await response.text();

        // Create new response with CORS headers
        const origin = request.headers.get('Origin') || '';
        const newHeaders = new Headers(response.headers);

        Object.entries(corsHeaders(origin)).forEach(([key, value]) => {
            newHeaders.set(key, value);
        });

        return new Response(responseBody, {
            status: response.status,
            statusText: response.statusText,
            headers: newHeaders
        });

    } catch (error) {
        return new Response(JSON.stringify({
            error: 'Backend unreachable',
            message: error.message
        }), {
            status: 502,
            headers: {
                'Content-Type': 'application/json',
                ...corsHeaders(request.headers.get('Origin') || '')
            }
        });
    }
}

// Main handler
addEventListener('fetch', event => {
    event.respondWith(handleRequest(event.request));
});

async function handleRequest(request) {
    const url = new URL(request.url);

    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
        return handleOptions(request);
    }

    // Health check
    if (url.pathname === '/health' || url.pathname === '/') {
        return new Response(JSON.stringify({
            status: 'online',
            service: 'KOF Ultimate Online API Gateway',
            version: '2.0.0',
            timestamp: new Date().toISOString()
        }), {
            headers: {
                'Content-Type': 'application/json',
                ...corsHeaders(request.headers.get('Origin') || '')
            }
        });
    }

    // Proxy all /api requests to backend
    if (url.pathname.startsWith('/api/')) {
        return proxyToBackend(request);
    }

    // Default response
    return new Response('KOF Ultimate Online - API Gateway', {
        headers: corsHeaders(request.headers.get('Origin') || '')
    });
}
