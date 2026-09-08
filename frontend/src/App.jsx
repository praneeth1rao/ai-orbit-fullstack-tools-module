import { Routes, Route } from "react-router-dom";
import Layout from "./layouts/Layout.jsx";
import ToolsListPage from "./pages/ToolsListPage.jsx";
import ToolDetailPage from "./pages/ToolDetailPage.jsx";
import NewToolPage from "./pages/NewToolPage.jsx";
import EditToolPage from "./pages/EditToolPage.jsx";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<ToolsListPage />} />
        <Route path="tools" element={<ToolsListPage />} />
        <Route path="tools/new" element={<NewToolPage />} />
        <Route path="tools/:id" element={<ToolDetailPage />} />
        <Route path="tools/:id/edit" element={<EditToolPage />} />
      </Route>
    </Routes>
  );
}
