import "./RaitingDinamics.scss";
import DownloadDashbord from "../../DownloadDashbord/DownloadDashbord.tsx";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";
import { data } from "../Compitents/Compitents.tsx";

function RaitingDinamics() {
  return (
    <div className="raiting-dinamics">
      <div className="raiting-dinamics__header">
        <div className="raiting-dinamics__download">
          <DownloadDashbord minimalism={true} />
        </div>
        <h2 className="raiting-dinamics__title">Динамика рейтинга</h2>
      </div>
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart
          width={500}
          height={400}
          data={data}
          margin={{
            top: 10,
            right: 0,
            left: 0,
            bottom: 0,
          }}
        >
          <defs>
            <linearGradient id="colorUv" x1="0" y1="0" x2="0" y2="1">
              <stop offset="30%" stopColor="#337DFF4D" stopOpacity={1} />
              <stop offset="95%" stopColor="#A8D4FF17" stopOpacity={0.9} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Area
            type="monotone"
            dataKey="uv"
            stroke="#002D97"
            fill="url(#colorUv)"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}

export default RaitingDinamics;
