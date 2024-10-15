import "./LineToolTip.scss";

const LineTooltip = ({ active, payload, name }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="line-tooltip">
        <p>
          {name}: {payload[0].value}
        </p>
      </div>
    );
  }

  return null;
};

export default LineTooltip;
