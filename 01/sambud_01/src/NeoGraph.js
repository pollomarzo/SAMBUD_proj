// lifted straight from https://github.com/jackdbd/react-neovis-example

import React, { useEffect, useRef } from "react";
import useResizeAware from "react-resize-aware";
import Neovis from "neovis.js/dist/neovis.js";

const NeoGraph = (props) => {
  const {
    width,
    height,
    containerId,
    backgroundColor,
    neo4jUri,
    neo4jUser,
    neo4jPassword,
    cypher,
  } = props;
  console.log(cypher);

  const visRef = useRef();

  useEffect(() => {
    const config = {
      container_id: visRef.current.id,
      server_url: neo4jUri,
      server_user: neo4jUser,
      server_password: neo4jPassword,
      labels: {},
      relationships: {},
      initial_cypher: cypher,
    };
    const vis = new Neovis(config);
    vis.render();
  }, [neo4jUri, neo4jUser, neo4jPassword, cypher]);

  return (
    <div
      id={containerId}
      ref={visRef}
      style={{
        width: `${width}px`,
        height: `${height}px`,
        backgroundColor: `${backgroundColor}`,
      }}
    />
  );
};

NeoGraph.defaultProps = {
  width: 600,
  height: 600,
  backgroundColor: "#d3d3d3",
};

const ResponsiveNeoGraph = (props) => {
  const [resizeListener, sizes] = useResizeAware();

  const side = Math.max(sizes.width, sizes.height);
  const neoGraphProps = { ...props, width: side, height: side };
  return (
    <div style={{ position: "relative" }}>
      {resizeListener}
      <NeoGraph {...neoGraphProps} />
    </div>
  );
};

ResponsiveNeoGraph.defaultProps = {
  backgroundColor: "#d3d3d3",
};

export { NeoGraph, ResponsiveNeoGraph };
