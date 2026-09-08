import { useState, useEffect } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { toolsApi, categoriesApi, APIError } from "../services/api";
import { PricingOptions, PlatformOptions, StatusOptions } from "../types";
import {
  FormInputField,
  FormTextareaField,
  FormSelectField,
  FormCheckboxesField,
  FormTagsField,
  FormUrlField,
} from "../components/FormFields";

export default function EditToolPage() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [categories, setCategories] = useState([]);
  const [tool, setTool] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [savingError, setSavingError] = useState(null);
  const [error, setError] = useState(null);

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [longDescription, setLongDescription] = useState("");
  const [categorySlug, setCategorySlug] = useState("");
  const [pricing, setPricing] = useState("free");
  const [platforms, setPlatforms] = useState([]);
  const [tags, setTags] = useState([]);
  const [websiteUrl, setWebsiteUrl] = useState("");
  const [status, setStatus] = useState("published");

  const [errors, setErrors] = useState({});

  useEffect(() => {
    let cancelled = false;

    const fetchData = async () => {
      try {
        const [toolData, categoriesData] = await Promise.all([
          toolsApi.get(id),
          categoriesApi.list(),
        ]);
        if (!cancelled) {
          setTool(toolData);
          setCategories(categoriesData);
          setTitle(toolData.title);
          setDescription(toolData.description);
          setLongDescription(toolData.long_description || "");
          setCategorySlug(toolData.category?.slug || "");
          setPricing(toolData.pricing);
          setPlatforms(Array.isArray(toolData.platforms) ? toolData.platforms : []);
          setTags(Array.isArray(toolData.tags) ? toolData.tags.map((t) => t.name) : []);
          setWebsiteUrl(toolData.website_url || "");
          setStatus(toolData.status);
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

    fetchData();
    return () => {
      cancelled = true;
    };
  }, [id]);

  const validate = () => {
    const newErrors = {};

    if (!title.trim()) {
      newErrors.title = "Title is required.";
    }

    if (!description.trim()) {
      newErrors.description = "Description is required.";
    }

    if (!categorySlug) {
      newErrors.category = "Please select a category.";
    }

    if (!pricing) {
      newErrors.pricing = "Please select a pricing option.";
    }

    if (!status) {
      newErrors.status = "Please select a status.";
    }

    if (websiteUrl) {
      try {
        new URL(websiteUrl);
      } catch {
        newErrors.websiteUrl = "Please enter a valid URL (e.g., example.com).";
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;

    setSaving(true);
    setSavingError(null);

    try {
      await toolsApi.update(id, {
        title: title.trim(),
        description: description.trim(),
        long_description: longDescription.trim() || null,
        category_slug: categorySlug || null,
        pricing,
        platforms: platforms.length > 0 ? platforms : null,
        tags: tags.length > 0 ? tags : null,
        website_url: websiteUrl || null,
        status,
        logo_url: null,
      });

      navigate(`/tools/${id}`, { replace: true });
    } catch (err) {
      setSavingError(err);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <section className="page tool-form-page">
        <div className="tool-form-header">
          <h1 className="tool-form-title">Edit tool</h1>
          <p className="tool-form-subtitle">
            Loading tool details…
          </p>
        </div>
        <div className="tool-form-loading">
          <div className="loading-state">
            <div className="loading-bar" />
            <p className="loading-text">Loading tool…</p>
          </div>
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section className="page tool-form-page">
        <div className="tool-form-header">
          <h1 className="tool-form-title">Edit tool</h1>
        </div>
        <div className="tool-form-error-state">
          <div className="error-state">
            <div className="error-icon">
              <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
                <circle cx="20" cy="20" r="18" stroke="currentColor" strokeWidth="1.5" />
                <path
                  d="M14 14l12 12M26 14l-12 12"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                />
              </svg>
            </div>
            <h3 className="error-title">
              {error instanceof APIError && error.status === 404
                ? "Tool not found"
                : "Could not load tool"}
            </h3>
            <p className="error-message">
              {error instanceof APIError && error.status === 404
                ? "This tool doesn’t exist or has been removed."
                : "We couldn’t load this tool right now."}
            </p>
            {error instanceof APIError && (
              <p className="error-detail">{error.message}</p>
            )}
            <div className="error-actions">
              <Link className="btn btn-primary" to="/tools">
                Back to Tools
              </Link>
            </div>
          </div>
        </div>
      </section>
    );
  }

  if (!tool) {
    return null;
  }

  return (
    <section className="page tool-form-page">
      <div className="tool-form-header">
        <div className="tool-form-nav">
          <Link className="btn btn-ghost" to={`/tools/${id}`}>
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
              <path
                d="M10 3l-6 5 6 5"
                stroke="currentColor"
                strokeWidth="1.75"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            Back to tool
          </Link>
        </div>
        <h1 className="tool-form-title">Edit tool</h1>
        <p className="tool-form-subtitle">
          Update the details for {tool.title}.
        </p>
      </div>

      <div className="tool-form-card">
        {savingError && (
          <div className="tool-form-error-banner">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="1.5" />
              <path
                d="M12 8v5M12 16h.01"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
              />
            </svg>
            <div>
              <p className="tool-form-error-text">
                {savingError instanceof APIError
                  ? savingError.message
                  : savingError?.message
                  ? savingError.message
                  : "Could not save changes. Please try again."}
              </p>
              <div className="tool-form-error-actions">
                <button
                  className="btn btn-secondary"
                  type="button"
                  onClick={() => setSavingError(null)}
                >
                  Dismiss
                </button>
              </div>
            </div>
          </div>
        )}

        <form className="tool-form" onSubmit={handleSubmit} noValidate>
          <div className="tool-form-section">
            <h2 className="tool-form-section-title">Basic information</h2>

            <div className="tool-form-grid">
              <FormInputField
                label="Title"
                value={title}
                onChange={(e) => {
                  setTitle(e.target.value);
                  if (errors.title) setErrors({ ...errors, title: null });
                }}
                error={errors.title}
                required
                placeholder="Enter the tool name"
              />

              <FormSelectField
                label="Category"
                value={categorySlug}
                onChange={(e) => {
                  setCategorySlug(e.target.value);
                  if (errors.category) setErrors({ ...errors, category: null });
                }}
                error={errors.category}
                required
                options={[
                  { label: "Select a category…", value: "" },
                  ...categories.map((c) => ({ label: c.name, value: c.slug })),
                ]}
              />

              <FormSelectField
                label="Pricing"
                value={pricing}
                onChange={(e) => {
                  setPricing(e.target.value);
                  if (errors.pricing) setErrors({ ...errors, pricing: null });
                }}
                error={errors.pricing}
                required
                options={PricingOptions.filter((p) => p.value !== "")}
              />

              <FormSelectField
                label="Status"
                value={status}
                onChange={(e) => {
                  setStatus(e.target.value);
                  if (errors.status) setErrors({ ...errors, status: null });
                }}
                error={errors.status}
                required
                options={StatusOptions}
              />
            </div>
          </div>

          <div className="tool-form-section">
            <h2 className="tool-form-section-title">Description</h2>

            <div className="tool-form-grid">
              <FormTextareaField
                label="Description"
                value={description}
                onChange={(e) => {
                  setDescription(e.target.value);
                  if (errors.description) setErrors({ ...errors, description: null });
                }}
                error={errors.description}
                required
                placeholder="A brief overview of the tool (shown in listings)"
                rows={3}
              />

              <div className="tool-form-full-width">
                <FormTextareaField
                  label="Long description"
                  value={longDescription}
                  onChange={(e) => setLongDescription(e.target.value)}
                  placeholder="A detailed description of the tool"
                  rows={6}
                />
              </div>
            </div>
          </div>

          <div className="tool-form-section">
            <h2 className="tool-form-section-title">Platforms & tags</h2>

            <div className="tool-form-grid">
              <FormCheckboxesField
                label="Platforms"
                value={platforms}
                onChange={setPlatforms}
                options={PlatformOptions}
              />

              <FormTagsField
                label="Tags"
                value={tags}
                onChange={setTags}
                placeholder="Type and press Enter to add…"
              />
            </div>
          </div>

          <div className="tool-form-section">
            <h2 className="tool-form-section-title">Links</h2>

            <div className="tool-form-grid">
              <FormUrlField
                label="Website URL"
                value={websiteUrl}
                onChange={(e) => {
                  setWebsiteUrl(e.target.value);
                  if (errors.websiteUrl) setErrors({ ...errors, websiteUrl: null });
                }}
                error={errors.websiteUrl}
                placeholder="example.com"
              />
            </div>
          </div>

          <div className="tool-form-footer">
            <div className="tool-form-actions">
              <Link className="btn btn-ghost" to={`/tools/${id}`}>
                Cancel
              </Link>
              <button
                className="btn btn-primary"
                type="submit"
                disabled={saving}
              >
                {saving ? (
                  <>
                    <span className="btn-spinner" />
                    Saving…
                  </>
                ) : (
                  "Save changes"
                )}
              </button>
            </div>
          </div>
        </form>
      </div>
    </section>
  );
}
