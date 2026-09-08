const API_BASE = "/api";

async function request(path, options = {}) {
  const url = `${API_BASE}${path}`;
  const res = await fetch(url, {
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
    ...options,
  });

  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = await res.json();
      detail =
        typeof body === "object" && body !== null
          ? body.detail || body.message || JSON.stringify(body)
          : body;
    } catch {
      try {
        detail = await res.text();
      } catch {
        detail = res.statusText;
      }
    }
    throw new APIError(res.status, detail);
  }

  return res.json();
}

export class APIError extends Error {
  constructor(status, detail) {
    super(detail);
    this.name = "APIError";
    this.status = status;
  }
}

export function get(path, init) {
  return request(path, init);
}

export function post(path, body, init) {
  return request(path, {
    method: "POST",
    body: JSON.stringify(body),
    ...init,
  });
}

export function put(path, body, init) {
  return request(path, {
    method: "PUT",
    body: JSON.stringify(body),
    ...init,
  });
}

export function remove(path, init) {
  return request(path, {
    method: "DELETE",
    ...init,
  });
}

export const toolsApi = {
  list(params) {
    const search = new URLSearchParams();
    if (params.q) search.set("q", params.q);
    if (params.category) search.set("category", params.category);
    if (params.pricing) search.set("pricing", params.pricing);
    if (params.platform) search.set("platform", params.platform);
    if (params.sort) search.set("sort", params.sort);
    if (params.page) search.set("page", String(params.page));
    if (params.limit) search.set("limit", String(params.limit));
    return get(`/tools?${search.toString()}`);
  },
  get(id) {
    return get(`/tools/${id}`);
  },
  create(body) {
    return post("/tools", body);
  },
  update(id, body) {
    return put(`/tools/${id}`, body);
  },
  delete(id) {
    return remove(`/tools/${id}`);
  },
};

export const categoriesApi = {
  list() {
    return get("/categories");
  },
};

export const tagsApi = {
  list() {
    return get("/tags");
  },
};
