import React, { useEffect, useState } from "react";

function WalletInsights() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("https://memes-watch.onrender.com/wallet-insights")
      .then((res) => res.json())
      .then(setData)
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      <h2>🔑 Wallet Insights</h2>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <table border="1" style={{ margin: "auto", width: "100%" }}>
          <thead>
            <tr>
              <th>Wallet</th>
              <th>Tx Count</th>
              <th>Last Active</th>
            </tr>
          </thead>
          <tbody>
            {data.map((d, i) => (
              <tr key={i}>
                <td>{d.wallet}</td>
                <td>{d.tx_count}</td>
                <td>{d.last_active}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default WalletInsights;