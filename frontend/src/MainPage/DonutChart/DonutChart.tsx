import DownloadDashbord from "../../DownloadDashbord/DownloadDashbord";
import "./DonutChart.scss";
import { PieChart, Pie, Cell, ResponsiveContainer, LabelList } from "recharts";

interface IProps {
  data: { name: string; value: number }[];
  title: string;
  colors: string[];
}

function DonutChart({ data, title, colors }: IProps) {
  return (
    <div className="donut">
      <div className="donut__header">
        <div>
          <DownloadDashbord minimalism={true} />
        </div>
        <h2 className="donut__title">{title}</h2>
      </div>
      <ResponsiveContainer width="100%" height="100%">
        <PieChart width={300} height={180}>
          <Pie
            data={data}
            cx={190}
            cy={100}
            innerRadius={60}
            outerRadius={80}
            fill="#8884d8"
            paddingAngle={5}
            dataKey="value"
            cornerRadius={10}
          >
            {data.map((item, index: any) => (
              <>
                <Cell
                  style={{ outline: "none" }}
                  key={`cell-${index}+${item.name}`}
                  fill={colors[index % colors.length]}
                  strokeWidth={0}
                />
              </>
            ))}
            <LabelList
              dataKey="name"
              position="outside"
              style={{ color: "black" }}
            />
          </Pie>
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

export default DonutChart;
