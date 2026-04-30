import React, { useEffect, useState } from "react";
import axios from "axios";

function LiveGraph() {
  const [img, setImg] = useState("");

  useEffect(() => {
    fetchGraph();

    const interval = setInterval(() => {
      fetchGraph();
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const fetchGraph = () => {
    axios.get("http://127.0.0.1:5000/graph")
      .then((res) => {
        setImg(
          res.data.graph + "?t=" + new Date().getTime()
        );
      })
      .catch((err) => console.log(err));
  };

  return (
    <div className="container mt-5 text-center">
      <h2>📈 Live Irrigation Graph</h2>

      {img ? (
        <img
          src={img}
          alt="Live Graph"
          style={{
            width: "90%",
            maxWidth: "900px",
            borderRadius: "12px",
            boxShadow: "0 4px 12px gray"
          }}
        />
      ) : (
        <h4>Loading Graph...</h4>
      )}
    </div>
  );
}

export default LiveGraph;