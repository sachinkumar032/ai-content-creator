import { useState, useEffect } from "react";
import {
  LineChart, Line, BarChart, Bar,
  XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer,
} from "recharts";

const MOCK_DATA = {
  overview: [
    { month: "Jan", views: 12400, subscribers: 340, videos: 14 },
    { month: "Feb", views: 28900, subscribers: 820, videos: 22 },
    { month: "Mar", views: 51200, subscribers: 1640, videos: 31 },
    { month: "Apr", views: 47800, subscribers: 1420, videos: 28 },
    { month: "May", views: 76300, subscribers: 2210, videos: 38 },
    { month: "Jun", views: 98400, subscribers: 3050, videos: 45 },
  ],
  platforms: [
    { name: "YouTube",   views: 54200, subs: 1820, videos: 45, color: "#CC0000" },
    { name: "TikTok",    views: 31600, subs: 980,  videos: 45, color: "#444444" },
    { name: "Instagram", views: 12600, subs: 250,  videos: 38, color: "#C13584" },
  ],
  recent: [
    { title: "5 Python Tricks Nobody Uses",  views: 14200, platform: "YouTube",   status: "live" },
    { title: "Build an AI Agent in 60s",      views: 8900,  platform: "TikTok",    status: "live" },
    { title: "Stop Writing Bad Loops",         views: 6100,  platform: "YouTube",   status: "live" },
    { title: "n8n Automation Full Guide",      views: 3200,  platform: "Instagram", status: "processing" },
  ],
};

// ── Replace with real API calls ───────────────────────────────────────────────
// function useAnalytics() {
//   const [data, setData] = useState(null);
//   useEffect(() => {
//     fetch("/api/analytics").then(r => r.json()).then(setData);
//   }, []);
//   return data ?? MOCK_DATA;
// }

const StatCard = ({ label, value, sub, accent = "#534AB7" }) => (
  <div style={{
    background: "#f8f7ff", borderRadius: 12,
    padding: "1.25rem 1.5rem", flex: 1, minWidth: 140,
  }}>
    <p style={{ fontSize: 11, color: "#888", margin: "0 0 6px",
      textTransform: "uppercase", letterSpacing: "0.07em", fontFamily: "monospace" }}>{label}</p>
    <p style={{ fontSize: 28, fontWeight: 700, margin: "0 0 2px", color: accent }}>{value}</p>
    {sub && <p style={{ fontSize: 12, color: "#999", margin: 0 }}>{sub}</p>}
  </div>
);

export default function Dashboard() {
  const [tab, setTab] = useState("overview");
  const d = MOCK_DATA;

  const totalViews = d.overview.reduce((s, r) => s + r.views, 0);
  const totalVideos = d.overview.reduce((s, r) => s + r.videos, 0);
  const totalSubs = d.overview[d.overview.length - 1].subscribers;

  return (
    <div style={{ fontFamily: "system-ui, sans-serif", padding: "1.5rem",
      maxWidth: 900, margin: "0 auto", color: "#1a1a1a" }}>

      <div style={{ display: "flex", justifyContent: "space-between",
        alignItems: "center", marginBottom: "1.5rem" }}>
        <div>
          <h1 style={{ fontSize: 22, fontWeight: 700, margin: 0 }}>Content Analytics</h1>
          <p style={{ fontSize: 13, color: "#888", margin: "4px 0 0",
            fontFamily: "monospace" }}>Autonomous pipeline · All platforms</p>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <div style={{ width: 8, height: 8, borderRadius: "50%", background: "#22c55e" }} />
          <span style={{ fontSize: 12, color: "#22c55e", fontFamily: "monospace" }}>Pipeline active</span>
        </div>
      </div>

      <div style={{ display: "flex", gap: 12, marginBottom: "1.5rem", flexWrap: "wrap" }}>
        <StatCard label="Total Views" value={totalViews.toLocaleString()} sub="all platforms" />
        <StatCard label="Subscribers" value={totalSubs.toLocaleString()} sub="+2,710 this month" accent="#0ea5e9" />
        <StatCard label="Videos Published" value={totalVideos} sub="fully automated" accent="#8b5cf6" />
        <StatCard label="Avg Engagement" value="6.4%" sub="+1.2% vs last month" accent="#f59e0b" />
      </div>

      <div style={{ display: "flex", gap: 4, marginBottom: "1.25rem",
        borderBottom: "1px solid #eee", paddingBottom: 8 }}>
        {["overview", "platforms", "recent"].map(t => (
          <button key={t} onClick={() => setTab(t)} style={{
            padding: "6px 16px", borderRadius: 8, border: "none", cursor: "pointer",
            fontSize: 13, fontWeight: 500, textTransform: "capitalize",
            background: tab === t ? "#534AB7" : "transparent",
            color: tab === t ? "#fff" : "#888",
          }}>{t}</button>
        ))}
      </div>

      {tab === "overview" && (
        <div style={{ display: "flex", flexDirection: "column", gap: "1.25rem" }}>
          <div style={{ background: "#f8f7ff", borderRadius: 12, padding: "1.25rem" }}>
            <p style={{ fontSize: 13, fontWeight: 600, margin: "0 0 1rem" }}>Views over time</p>
            <ResponsiveContainer width="100%" height={200}>
              <LineChart data={d.overview}>
                <CartesianGrid strokeDasharray="3 3" stroke="#eee" />
                <XAxis dataKey="month" tick={{ fontSize: 11 }} />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip />
                <Line type="monotone" dataKey="views" stroke="#534AB7" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
          <div style={{ background: "#f8f7ff", borderRadius: 12, padding: "1.25rem" }}>
            <p style={{ fontSize: 13, fontWeight: 600, margin: "0 0 1rem" }}>Videos published per month</p>
            <ResponsiveContainer width="100%" height={160}>
              <BarChart data={d.overview}>
                <CartesianGrid strokeDasharray="3 3" stroke="#eee" />
                <XAxis dataKey="month" tick={{ fontSize: 11 }} />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip />
                <Bar dataKey="videos" fill="#AFA9EC" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {tab === "platforms" && (
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          {d.platforms.map(p => (
            <div key={p.name} style={{
              background: "#f8f7ff", borderRadius: 12,
              padding: "1rem 1.25rem", display: "flex", alignItems: "center", gap: "1rem",
            }}>
              <div style={{
                width: 40, height: 40, borderRadius: 10, display: "flex",
                alignItems: "center", justifyContent: "center",
                background: p.color + "18", fontWeight: 700, fontSize: 13, color: p.color,
              }}>{p.name[0]}</div>
              <div style={{ flex: 1 }}>
                <p style={{ margin: 0, fontWeight: 600, fontSize: 14 }}>{p.name}</p>
                <p style={{ margin: "2px 0 0", fontSize: 12, color: "#999",
                  fontFamily: "monospace" }}>{p.videos} videos uploaded</p>
              </div>
              <div style={{ textAlign: "right" }}>
                <p style={{ margin: 0, fontWeight: 700, fontSize: 16 }}>{p.views.toLocaleString()}</p>
                <p style={{ margin: "2px 0 0", fontSize: 11, color: "#999" }}>views</p>
              </div>
              <div style={{ textAlign: "right", minWidth: 60 }}>
                <p style={{ margin: 0, fontWeight: 700, fontSize: 16, color: "#22c55e" }}>
                  +{p.subs.toLocaleString()}
                </p>
                <p style={{ margin: "2px 0 0", fontSize: 11, color: "#999" }}>subs</p>
              </div>
            </div>
          ))}
        </div>
      )}

      {tab === "recent" && (
        <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
          {d.recent.map((v, i) => (
            <div key={i} style={{
              background: "#f8f7ff", borderRadius: 12,
              padding: "1rem 1.25rem", display: "flex", alignItems: "center", gap: "1rem",
            }}>
              <div style={{ flex: 1 }}>
                <p style={{ margin: 0, fontWeight: 600, fontSize: 14 }}>{v.title}</p>
                <p style={{ margin: "3px 0 0", fontSize: 12, color: "#999",
                  fontFamily: "monospace" }}>{v.platform}</p>
              </div>
              <div style={{ textAlign: "right" }}>
                <p style={{ margin: 0, fontWeight: 700 }}>{v.views.toLocaleString()}</p>
                <p style={{ margin: "2px 0 0", fontSize: 11, color: "#999" }}>views</p>
              </div>
              <span style={{
                fontSize: 11, padding: "3px 10px", borderRadius: 99,
                fontFamily: "monospace",
                background: v.status === "live" ? "#dcfce7" : "#fef9c3",
                color: v.status === "live" ? "#15803d" : "#a16207",
              }}>{v.status}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
