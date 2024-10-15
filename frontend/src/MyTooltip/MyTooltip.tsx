import "./MyTooltip.scss";

interface IProps {
  showTooltip: boolean;
  text: string;
}

function MyTooltip({ showTooltip, text }: IProps) {
  return (
    <div className="tooltip-container">
      {showTooltip && (
        <div className="tooltip">
          <div className="tooltip-arrow" />
          <div className="tooltip-text">{text}</div>
        </div>
      )}
    </div>
  );
}

export default MyTooltip;
