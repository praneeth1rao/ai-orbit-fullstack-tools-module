import { useState, useEffect, useCallback, useRef } from "react";
import { useNavigate, Link } from "react-router-dom";
import { toolsApi, categoriesApi } from "../services/api";
import { APIError } from "../services/api";
import SearchBar from "../components/SearchBar";
import FilterBar from "../components/FilterBar";
import ToolCard from "../components/ToolCard";
import Pagination from "../components/Pagination";
import LoadingState from "../components/LoadingState";
import EmptyState from "../components/EmptyState";
import ErrorState from "../components/ErrorState";

const DEFAULT_LIMIT = 12;

export default function ToolsListPage() {
  const navigate = useNavigate();

  const [categories, setCategories] = useState([]);
  const [tools, setTools] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [total, setTotal] = useState(0);

  const [q, setQ] = useState("");
  const [category, setCategory] = useState("");
  const [pricing, setPricing] = useState("");
  const [platforms, setPlatforms] = useState([]);
  const [sort, setSort] = useState("newest");

  const [searchLocal, setSearchLocal] = useState("");
  const searchTimerRef = useRef(null);

  const fetchTools = useCallback(
    async (pageNo, overrides = {}) => {
      setLoading(true);
      setError(null);
      try {
        const data = await toolsApi.list({
          q: overrides.q ?? q,
          category: overrides.category ?? category,
          pricing: overrides.pricing ?? pricing,
          platform: overrides.platform ?? platforms.join(","),
          sort: overrides.sort ?? sort,
          page: pageNo,
          limit: DEFAULT_LIMIT,
        });
        setTools(data.tools);
        setTotalPages(data.pagination.total_pages);
        setTotal(data.pagination.total);
        const finalPage = data.pagination.page;
        setPage(finalPage);
        if (data.pagination.total_pages && finalPage > data.pagination.total_pages) {
          setPage(data.pagination.total_pages);
        }
      } catch (err) {
        setTools([]);
        if (err instanceof APIError && err.status === 404) {
          setError("tools_not_found");
        } else {
          setError(err);
        }
      } finally {
        setLoading(false);
      }
    },
    [q, category, pricing, platforms, sort]
  );

  const loadPage = useCallback(
    (pageNo) => {
      if (pageNo < 1) pageNo = 1;
      if (!totalPages || pageNo > totalPages) {
        fetchTools(pageNo);
        return;
      }
      fetchTools(pageNo);
    },
    [fetchTools, totalPages]
  );

  useEffect(() => {
    categoriesApi.list().then(setCategories).catch(() => setCategories([]));
  }, []);

  useEffect(() => {
    setPage(1);
    fetchTools(1);
  }, [q, category, pricing, platforms.join(","), sort, fetchTools]);

  const clearFilters = () => {
    setQ("");
    setSearchLocal("");
    setCategory("");
    setPricing("");
    setPlatforms([]);
    setSort("newest");
    setPage(1);
  };

  const hasActiveFilters =
    Boolean(category) ||
    Boolean(pricing) ||
    platforms.length > 0 ||
    q.trim().length > 0;

  const handleSearchChange = (value) => {
    setSearchLocal(value);
    if (searchTimerRef.current) clearTimeout(searchTimerRef.current);
    searchTimerRef.current = setTimeout(() => {
      setQ(value);
      setPage(1);
    }, 280);
  };

  const goToPage = (next) => {
    const target = next ?? page + 1;
    if (target < 1 || (totalPages && target > totalPages)) return;
    loadPage(target);
  };

  const retry = () => loadPage(page);

  if (loading && tools.length === 0) {
    return (
      <section className="page tools-page">
        <div className="tools-header">
          <h1 className="tools-title">Tools</h1>
          <p className="tools-subtitle">
            Discover AI tools curated for real workflows.
          </p>
        </div>
        <LoadingState text="Loading tools…" />
      </section>
    );
  }

  if (error && !loading) {
    return (
      <section className="page tools-page">
        <div className="tools-header">
          <h1 className="tools-title">Tools</h1>
          <p className="tools-subtitle">
            Discover AI tools curated for real workflows.
          </p>
        </div>
        <ErrorState
          message={
            error === "tools_not_found"
              ? "No tools matched the current request."
              : "We couldn’t load the tools right now."
          }
          errorText={
            error?.message && error !== "tools_not_found"
              ? error.message
              : undefined
          }
          onRetry={retry}
        />
      </section>
    );
  }

  if (!loading && tools.length === 0 && !error) {
    return (
      <section className="page tools-page">
        <div className="tools-header">
          <h1 className="tools-title">Tools</h1>
          <p className="tools-subtitle">
            Discover AI tools curated for real workflows.
          </p>
        </div>
        <EmptyState
          title="No tools found"
          message={
            hasActiveFilters
              ? "Try adjusting your search or filters."
              : "No tools have been added yet."
          }
          action={
            !hasActiveFilters ? (
              <a className="btn btn-primary" href="/tools/new">
                Add the first tool
              </a>
            ) : (
              <button className="btn" type="button" onClick={clearFilters}>
                Clear filters
              </button>
            )
          }
        />
      </section>
    );
  }

  return (
    <section className="page tools-page">
      <div className="tools-header">
        <h1 className="tools-title">Tools</h1>
        <p className="tools-subtitle">
          Discover AI tools curated for real workflows.
        </p>
      </div>

      <div className="tools-controls">
        <SearchBar
          value={searchLocal}
          onChange={handleSearchChange}
          placeholder="Search tools..."
          autoFocus
        />
      </div>

      <FilterBar
        categories={categories}
        selectedCategory={category}
        onCategoryChange={(next) => {
          setCategory(next);
          setPage(1);
        }}
        selectedPricing={pricing}
        onPricingChange={(next) => {
          setPricing(next);
          setPage(1);
        }}
        selectedPlatforms={platforms}
        onPlatformsChange={(next) => {
          setPlatforms(next);
          setPage(1);
        }}
        selectedSort={sort}
        onSortChange={(next) => {
          setSort(next);
          setPage(1);
        }}
        onClearFilters={clearFilters}
        activeFilterCount={
          (category ? 1 : 0) +
          (pricing ? 1 : 0) +
          platforms.length +
          (q.trim().length > 0 ? 1 : 0)
        }
      />

      <div className="tools-results-bar">
        <span className="tools-count">
          {total} tool{total !== 1 ? "s" : ""}
        </span>
        <Link className="btn btn-primary" to="/tools/new">
          Add tool
        </Link>
      </div>

      <div className="tools-grid">
        {tools.map((tool) => (
          <ToolCard
            key={tool.id}
            tool={tool}
            onClick={() => navigate(`/tools/${tool.id}`)}
          />
        ))}
      </div>

      <Pagination page={page} totalPages={totalPages} onPageChange={goToPage} />
    </section>
  );
}
