"use client";
import { useEffect, useMemo, useState } from "react";
import {
  Background,
  BackgroundVariant,
  Controls,
  Handle,
  MarkerType,
  Position,
  ReactFlow,
  useReactFlow,
  type Edge,
  type Node,
  type NodeProps,
} from "@xyflow/react";
import dagre from "@dagrejs/dagre";
import { AnimatePresence, motion } from "framer-motion";
import "@xyflow/react/dist/style.css";

type NodeType = "query" | "control" | "policy" | "infra" | "doc" | "message" | "employee";

export type Trace = {
  logs: string[];
  nodes: { id: string; label: string; type: NodeType; layer: 0 | 1 | 2 }[];
  edges: { from: string; to: string; rel: string }[];
};

const C: Record<NodeType, string> = {
  query: "#2c261e", control: "#b56f3e", policy: "#4f8a5b",
  infra: "#7c6a9a", doc: "#3d7a8c", message: "#c4842a", employee: "#b06a8a",
};

const KIND: Record<NodeType, string> = {
  query: "asked", control: "control", policy: "policy",
  infra: "infra", doc: "document", message: "message", employee: "person",
};

const NW = 196;
const NH = 44;

// "risk_management_policy_v1.0.md:L139-L151" → name + line range shown separately
function split(label: string) {
  const m = /^(.*?):(L\d+(?:[-–]L?\d+)?)$/.exec(label);
  return m ? { name: m[1], lines: m[2] } : { name: label, lines: "" };
}

type Data = { label: string; kind: NodeType } & Record<string, unknown>;
type TNode = Node<Data, "trace">;

function TraceNode({ data }: NodeProps<TNode>) {
  const { name, lines } = split(data.label);
  return (
    <motion.div
      className="tnode"
      style={{ ["--c" as string]: C[data.kind], width: NW, height: NH }}
      initial={{ opacity: 0, scale: 0.8, filter: "blur(4px)" }}
      animate={{ opacity: 1, scale: 1, filter: "blur(0px)" }}
      transition={{ type: "spring", stiffness: 280, damping: 22 }}
    >
      <Handle type="target" position={Position.Left} className="thandle" />
      <span className="tdot" />
      <span className="tbody">
        <span className="tkind">
          {KIND[data.kind]}
          {lines && <em>{lines}</em>}
        </span>
        <span className="tlabel" title={data.label}>{name}</span>
      </span>
      <Handle type="source" position={Position.Right} className="thandle" />
    </motion.div>
  );
}

const NODE_TYPES = { trace: TraceNode };

function FitView({ dep }: { dep: number }) {
  const flow = useReactFlow();
  useEffect(() => {
    const t = setTimeout(
      () => void flow.fitView({ padding: 0.14, maxZoom: 1, duration: 480 }),
      40,
    );
    return () => clearTimeout(t);
  }, [dep, flow]);
  return null;
}

export default function GraphTrace({ trace, live }: { trace: Trace; live?: boolean }) {
  const [shown, setShown] = useState(live ? 0 : trace.logs.length);

  useEffect(() => {
    if (!live) return;
    setShown(0);
    const t = setInterval(
      () => setShown((s) => (s >= trace.logs.length ? (clearInterval(t), s) : s + 1)),
      150,
    );
    return () => clearInterval(t);
  }, [live, trace]);

  const revealed = trace.logs.slice(0, shown);
  const logsDone = shown >= trace.logs.length;

  // Stable dagre layout for the whole graph, computed once per trace, so nodes
  // keep their position while they stream in one by one.
  const { positioned, order, height } = useMemo(() => {
    const g = new dagre.graphlib.Graph();
    g.setDefaultEdgeLabel(() => ({}));
    g.setGraph({ rankdir: "LR", ranksep: 104, nodesep: 20, marginx: 22, marginy: 22 });
    trace.nodes.forEach((n) => g.setNode(n.id, { width: NW, height: NH }));
    trace.edges.forEach((e) => {
      if (g.hasNode(e.from) && g.hasNode(e.to)) g.setEdge(e.from, e.to);
    });
    dagre.layout(g);

    let maxY = 0;
    const positioned: TNode[] = trace.nodes.map((n) => {
      const p = g.node(n.id);
      maxY = Math.max(maxY, p.y + NH / 2);
      return {
        id: n.id,
        type: "trace" as const,
        position: { x: p.x - NW / 2, y: p.y - NH / 2 },
        data: { label: n.label, kind: n.type },
        draggable: false,
        connectable: false,
      };
    });

    const order = [...trace.nodes]
      .sort((a, b) => a.layer - b.layer)
      .map((n) => n.id);

    return { positioned, order, height: Math.min(560, Math.max(230, maxY + 48)) };
  }, [trace]);

  const [visible, setVisible] = useState(live ? 0 : order.length);

  useEffect(() => {
    if (!logsDone) return;
    if (!live) return setVisible(order.length);
    setVisible(0);
    const t = setInterval(
      () => setVisible((v) => (v >= order.length ? (clearInterval(t), v) : v + 1)),
      95,
    );
    return () => clearInterval(t);
  }, [logsDone, live, order.length]);

  const live_ids = useMemo(
    () => new Set(order.slice(0, visible)),
    [order, visible],
  );

  const nodes = useMemo(
    () => positioned.filter((n) => live_ids.has(n.id)),
    [positioned, live_ids],
  );

  const edges: Edge[] = useMemo(
    () =>
      trace.edges
        .filter((e) => live_ids.has(e.from) && live_ids.has(e.to))
        .map((e, i) => {
          const bad = /CONTRADICT|CONFLICT/i.test(e.rel);
          const color = bad ? "#c4842a" : "#c3b39c";
          return {
            id: `e${i}`,
            source: e.from,
            target: e.to,
            type: "default",
            animated: true,
            label: e.rel.toLowerCase().replace(/_/g, " "),
            labelShowBg: true,
            labelBgPadding: [6, 3] as [number, number],
            labelBgBorderRadius: 6,
            labelBgStyle: { fill: "#fbf7f0", fillOpacity: 0.92 },
            labelStyle: {
              fill: bad ? "#a8672a" : "#8a8074",
              fontSize: 9,
              fontFamily: "ui-monospace, SFMono-Regular, monospace",
              letterSpacing: "0.05em",
            },
            style: {
              stroke: color,
              strokeWidth: bad ? 1.6 : 1.3,
              strokeDasharray: bad ? "5 4" : undefined,
            },
            markerEnd: { type: MarkerType.ArrowClosed, color, width: 14, height: 14 },
          };
        }),
    [trace.edges, live_ids],
  );

  const kinds = useMemo(
    () => Array.from(new Set(trace.nodes.map((n) => n.type))),
    [trace.nodes],
  );

  return (
    <div className="gt">
      {logsDone && positioned.length > 0 && (
        <motion.div
          className="gcanvas"
          style={{ height }}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3 }}
        >
          <ReactFlow
            nodes={nodes}
            edges={edges}
            nodeTypes={NODE_TYPES}
            fitView
            fitViewOptions={{ padding: 0.14, maxZoom: 1 }}
            minZoom={0.3}
            maxZoom={1.8}
            nodesDraggable={false}
            nodesConnectable={false}
            elementsSelectable={false}
            panOnScroll
            zoomOnScroll={false}
            proOptions={{ hideAttribution: true }}
          >
            <Background variant={BackgroundVariant.Dots} gap={22} size={1.1} color="#ddd0bd" />
            <Controls showInteractive={false} position="top-right" />
            <FitView dep={visible} />
          </ReactFlow>

          <div className="glegend">
            {kinds.map((k) => (
              <span key={k} style={{ ["--c" as string]: C[k] }}>
                <i />
                {KIND[k]}
              </span>
            ))}
            <b>
              {trace.nodes.length} nodes · {trace.edges.length} edges
            </b>
          </div>
        </motion.div>
      )}

      <div className="glog">
        <AnimatePresence initial={false}>
          {revealed.map((l, i) => (
            <motion.div
              key={i}
              className={`gline ${l.startsWith("  ") ? "sub" : ""}
                ${/CONFLICT|DISAGREE/i.test(l) ? "warn" : ""}
                ${/verdict/i.test(l) ? "verdict" : ""}`}
              initial={{ opacity: 0, x: -6 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.18, ease: "easeOut" }}
            >
              <span className="gt-caret">{l.startsWith("  ") ? "" : "›"}</span>
              {l.trim()}
            </motion.div>
          ))}
        </AnimatePresence>
        {!logsDone && <div className="gline cursor">▌</div>}
      </div>
    </div>
  );
}
