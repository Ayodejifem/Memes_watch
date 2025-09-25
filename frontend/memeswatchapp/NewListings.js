import React, { useEffect, useState } from "react";

function NewListings() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${process.env.REACT_APP_API_URL}/new-listings`)
      .then((res) => res.json())
      .then(setData)
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      <h2>🐦 New Listings</h2>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <table border="1" style={{ margin: "auto", width: "100%" }}>
          <thead>
            <tr>
              <th>Token</th>
              <th>Exchange</th>
              <th>Price</th>
              <th>Volume</th>
            </tr>
          </thead>
          <tbody>
            {data.map((d, i) => (
              <tr key={i}>
                <td>{d.token}</td>
                <td>{d.exchange}</td>
                <td>{d.price}</td>
                <td>{d.volume}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default NewListings;