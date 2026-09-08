import { useState, useEffect } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { toolsApi, APIError } from "../services/api";
import LoadingState from "../components/LoadingState";
import ErrorState from "../components/ErrorState";
import EmptyState from "../components/EmptyState";

export default function ToolDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [tool, setTool] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;

    const fetchTool = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await toolsApi.get(id);
        if (!cancelled) {
          setTool(data);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    };

    fetchTool();
    return () => {
      cancelled = true;
    };
  }, [id]);

  if (loading) {
    return (
      <section className="page tool-detail-page">
        <div className="tool-detail-header">
          <h1 className="tools-title">Tool details</h1>
          <p className="tools-subtitle">
            View details for this AI tool.
          </p>
        </div>
        <LoadingState text="Loading tool…" />
      </section>
    );
  }

  if (error) {
    return (
      <section className="page tool-detail-page">
        <div className="tool-detail-header">
          <h1 className="tools-title">Tool details</h1>
          <p className="tools-subtitle">
            View details for this AI tool.
          </p>
        </div>
        <ErrorState
          message={
            error instanceof APIError && error.status === 404
              ? "This tool doesn’t exist or has been removed."
              : "We couldn’t load this tool right now."
          }
          errorText={
            error instanceof APIError
              ? error.message
              : error?.message
              ? error.message
              : undefined
          }
          onRetry={() => navigate(`/tools/${id}`, { replace: true })}
        />
      </section>
    );
  }

  if (!tool) {
    return (
      <section className="page tool-detail-page">
        <div className="tool-detail-header">
          <h1 className="tools-title">Tool details</h1>
          <p className="tools-subtitle">
            View details for this AI tool.
          </p>
        </div>
        <EmptyState
          title="Tool not found"
          message="We couldn’t find a tool with this address."
        />
      </section>
    );
  }

  const platforms = Array.isArray(tool.platforms)
    ? tool.platforms
    : (tool.platforms || ["web"]).filter(Boolean);

  const safeWebsiteUrl = tool.website_url
    ? tool.website_url.replace(/^https?:\/\//, "").replace(/\/.*$/, "")
    : null;

  return (
    <section className="page tool-detail-page">
      <header className="tool-detail-header">
        <div className="tool-detail-nav">
          <button
            className="btn btn-ghost"
            type="button"
            onClick={() => navigate("/tools")}
          >
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
              <path
                d="M10 3l-6 5 6 5"
                stroke="currentColor"
                strokeWidth="1.75"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            Back to Tools
          </button>
        </div>

        <div className="tool-detail-hero">
          <div className="tool-detail-logo">
            {tool.logo_url ? (
              <img
                className="tool-logo"
                src={tool.logo_url}
                alt={`${tool.title} logo`}
                loading="eager"
              />
            ) : (
              <div className="tool-logo-placeholder" aria-hidden="true">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none">
                  <path
                    d="M8 18L12 8L16 18"
                    stroke="currentColor"
                    strokeWidth="1.8"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              </div>
            )}
          </div>

          <div className="tool-detail-title-block">
            <h1 className="tool-detail-title">{tool.title}</h1>
            {tool.category && (
              <span className="tool-chip">{tool.category.name}</span>
            )}
            <span className={`tool-chip tool-chip-pricing tool-chip-${tool.pricing}`}>
              {tool.pricing}
            </span>
          </div>

          {tool.website_url && (
            <a
              className="tool-detail-website"
              href={tool.website_url}
              target="_blank"
              rel="noopener noreferrer"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                <path
                  d="M3 8a1 1 0 011-1h16a1 1 0 011 1v11a1 1 0 01-1 1h-3.5l-1-1H12l-2.5-2.5A1 1 0 018 17V8a1 1 0 011-1h4a1 1 0 011 1v2h3a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1v-2a1 1 0 011-1h1V8z"
                  stroke="currentColor"
                  strokeWidth="1.8"
                  strokeLinejoin="round"
                />
              </svg>
              {safeWebsiteUrl}
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                <path
                  d="M7 13l3 3 7-7"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </a>
          )}
        </div>
      </header>

      <div className="tool-detail-layout">
        <div className="tool-detail-main">
          <section className="tool-detail-section">
            <h2 className="tool-detail-section-title">Overview</h2>
            <p className="tool-detail-description">{tool.description}</p>
          </section>

          {tool.long_description && (
            <section className="tool-detail-section">
              <h2 className="tool-detail-section-title">Description</h2>
              <p className="tool-detail-long-description">
                {tool.long_description}
              </p>
            </section>
          )}

          {platforms.length > 0 && (
            <section className="tool-detail-section">
              <h2 className="tool-detail-section-title">Platforms</h2>
              <ul className="tool-detail-platform-list">
                {platforms.map((p) => (
                  <li key={p} className="tool-detail-platform-item">
                    {p}
                  </li>
                ))}
              </ul>
            </section>
          )}

          {tool.tags && tool.tags.length > 0 && (
            <section className="tool-detail-section">
              <h2 className="tool-detail-section-title">Tags</h2>
              <ul className="tag-list">
                {tool.tags.map((tag) => (
                  <li key={tag.id ?? tag.slug} className="tag-item">
                    {tag.name}
                  </li>
                ))}
              </ul>
            </section>
          )}
        </div>

        <aside className="tool-detail-sidebar">
          <div className="tool-detail-meta-card">
            <h3 className="tool-detail-meta-title">Details</h3>

            <dl className="tool-detail-meta-list">
              {tool.category && (
                <div className="tool-detail-meta-item">
                  <dt className="tool-detail-meta-label">Category</dt>
                  <dd className="tool-detail-meta-value">
                    {tool.category.name}
                  </dd>
                </div>
              )}

              <div className="tool-detail-meta-item">
                <dt className="tool-detail-meta-label">Pricing</dt>
                <dd className={`tool-chip tool-chip-pricing tool-chip-${tool.pricing}`}>
                  {tool.pricing}
                </dd>
              </div>

              <div className="tool-detail-meta-item">
                <dt className="tool-detail-meta-label">Website</dt>
                <dd className="tool-detail-meta-value">
                  {tool.website_url ? (
                    <a
                      className="tool-detail-meta-link"
                      href={tool.website_url}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      {safeWebsiteUrl}
                      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                        <path
                          d="M7 13l3 3 7-7"
                          stroke="currentColor"
                          strokeWidth="2"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        />
                      </svg>
                    </a>
                  ) : (
                    <span className="tool-detail-meta-empty">Not provided</span>
                  )}
                </dd>
              </div>

              <div className="tool-detail-meta-item">
                <dt className="tool-detail-meta-label">Created</dt>
                <dd className="tool-detail-meta-value">
                  {formatDate(tool.created_at)}
                </dd>
              </div>

              <div className="tool-detail-meta-item">
                <dt className="tool-detail-meta-label">Last updated</dt>
                <dd className="tool-detail-meta-value">
                  {formatDate(tool.updated_at)}
                </dd>
              </div>

              <div className="tool-detail-meta-item">
                <dt className="tool-detail-meta-label">Status</dt>
                <dd className={`tool-chip tool-chip-status tool-chip-${tool.status}`}>
                  {tool.status}
                </dd>
              </div>
            </dl>
          </div>

          {tool.id && (
            <div className="tool-detail-meta-card">
              <h3 className="tool-detail-meta-title">Actions</h3>
              <div className="tool-detail-actions">
                <Link className="btn btn-secondary" to={`/tools/${tool.id}/edit`}>
                  Edit tool
                </Link>
              </div>
            </div>
          )}
        </aside>
      </div>
    </section>
  );
}

function formatDate(date) {
  if (!date) return "";
  const d = new Date(date);
  if (isNaN(d.getTime())) return String(date);
  return d.toLocaleDateString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}
