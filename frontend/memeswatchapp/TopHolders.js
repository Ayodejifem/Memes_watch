import React, { useEffect, useState } from "react";

function TopHolders() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${process.env.REACT_APP_API_URL}/top-holders`)
      .then((res) => res.json())
      .then(setData)
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      <h2>🐳 Token Top Holders</h2>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <table border="1" style={{ margin: "auto", width: "100%" }}>
          <thead>
            <tr>
              <th>Holder</th>
              <th>Token</th>
              <th>Balance</th>
            </tr>
          </thead>
          <tbody>
            {data.map((d, i) => (
              <tr key={i}>
                <td>{d.holder}</td>
                <td>{d.token}</td>
                <td>{d.balance}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default TopHolders;