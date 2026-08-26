export function SkeletonLine({ width = "100%" }) {
  return <div className="skeleton skel-line" style={{ width }} />;
}

export function SkeletonRows({ rows = 5, cols = 5 }) {
  return (
    <>
      {Array.from({ length: rows }).map((_, r) => (
        <tr className="skel-row" key={r}>
          {Array.from({ length: cols }).map((__, c) => (
            <td key={c}>
              <SkeletonLine width={c === 0 ? "70%" : "50%"} />
            </td>
          ))}
        </tr>
      ))}
    </>
  );
}

export function SkeletonStatStrip({ count = 4 }) {
  return (
    <div className="stat-strip">
      {Array.from({ length: count }).map((_, i) => (
        <div className="stat-cell" key={i}>
          <SkeletonLine width="60%" />
          <div style={{ height: 10 }} />
          <SkeletonLine width="40%" />
        </div>
      ))}
    </div>
  );
}
