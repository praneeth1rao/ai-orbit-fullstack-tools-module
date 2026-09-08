export default function ToolCard({ tool, onClick }) {
  const platforms = Array.isArray(tool.platforms)
    ? tool.platforms
    : (tool.platforms || "web").split(",").map((p) => p.trim()).filter(Boolean);

  return (
    <article className="tool-card" onClick={onClick}>
      <div className="tool-card-thumb">
        {tool.logo_url ? (
          <img
            className="tool-logo"
            src={tool.logo_url}
            alt={`${tool.title} logo`}
            loading="lazy"
          />
        ) : (
          <div className="tool-logo-placeholder" aria-hidden="true">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
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

      <div className="tool-card-body">
        <div className="tool-card-meta">
          {tool.category && (
            <span className="tool-chip">{tool.category.name}</span>
          )}
          <span className={`tool-chip tool-chip-pricing tool-chip-${tool.pricing}`}>
            {tool.pricing}
          </span>
        </div>

        <h3 className="tool-title">{tool.title}</h3>
        <p className="tool-description">{tool.description}</p>

        <div className="tool-tags">
          {tool.tags && tool.tags.length > 0 && (
            <ul className="tag-list">
              {tool.tags.slice(0, 4).map((tag) => (
                <li key={tag.id ?? tag.slug} className="tag-item">
                  {tag.name}
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>

      <div className="tool-card-footer">
        <span className="tool-platforms">
          {platforms.map((p) => (
            <span key={p} className="platform-tag">
              {p}
            </span>
          ))}
        </span>
      </div>
    </article>
  );
}
