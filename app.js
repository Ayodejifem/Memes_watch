import React, { useState } from "react";
import NewListings from "./components/NewListings";
import TopHolders from "./components/TopHolders";
import WalletInsights from "./components/WalletInsights";

function App() {
  const [page, setPage] = useState("home");

  return (
    <div style={{ fontFamily: "Inter, sans-serif", maxWidth: 900, margin: "auto", padding: 24 }}>
      <h1 style={{ textAlign: "center" }}>🚀 MemesWatch Dashboard</h1>
      <nav style={{ textAlign: "center", marginBottom: 32 }}>
        <button onClick={() => setPage("new-listings")}>🐦 New Listings</button>{" "}
        <button onClick={() => setPage("top-holders")}>🐳 Token Top Holders</button>{" "}
        <button onClick={() => setPage("wallet-insights")}>🔑 Wallet Insights</button>
      </nav>
      {page === "home" && (
        <div style={{ textAlign: "center" }}>
          <p>Welcome! Choose a section above.</p>
        </div>
      )}
      {page === "new-listings" && <NewListings />}
      {page === "top-holders" && <TopHolders />}
      {page === "wallet-insights" && <WalletInsights />}
    </div>
  );
}

export default App;