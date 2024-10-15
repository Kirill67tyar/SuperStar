import "./StaticCards.scss";
import progressArrowUp from "../../assets/icons/progress-arrow-up.svg";
import progressArrowDown from "../../assets/icons/progress-arrow-down.svg";
import { Link } from "react-router-dom";

function StaticCards() {
  return (
    <ul className="static-cards">
      <li className="static-card">
        <div className="static-card__value">3</div>
        <h3 className="static-card__title">Bus factor</h3>
      </li>
      <li className="static-card">
        <div className="static-card__data">
          <div className="static-card__value">62%</div>
          <div className="static-card__progress">
            <img
              className="static-card__progress-arrow"
              src={progressArrowUp}
              alt="progress arrow"
            />
            <div className="static-card__progress-data">12 %</div>
          </div>
        </div>
        <h3 className="static-card__title">соответствие текущей роли</h3>
      </li>
      <li className="static-card">
        <Link className="static-card__link" to="/training-request">
          <div className="static-card__value">10</div>
          <h3 className="static-card__title">запросов на обучение</h3>
        </Link>
      </li>
      <li className="static-card static-card__progress-bar">
        <div className="static-card__data">
          <div className="static-card__value">4/18</div>
          <div className="static-card__progress">
            <img
              className="static-card__progress-arrow"
              src={progressArrowDown}
              alt="progress arrow"
            />
            <div className="static-card__progress-data">12 %</div>
          </div>
        </div>
        <div>
          <h3 className="static-card__title">Планы развития</h3>
          <div className="progress-bar">
            <div
              className="progress-bar__fill"
              id="progressBarFill"
              style={{ width: "70%" }}
            ></div>
          </div>
          <p className="progress-bar__subtitle">Выполненно 70%</p>
        </div>
      </li>
    </ul>
  );
}

export default StaticCards;
