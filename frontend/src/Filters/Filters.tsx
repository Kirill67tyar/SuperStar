import { v4 as uuidv4 } from "uuid";
import DownloadDashbord from "../DownloadDashbord/DownloadDashbord";
import FilterItem from "./FilterItem/FilterItem";
import delCross from "../assets/icons/delete-cross.svg";
import "./Filters.scss";

function Filters() {
  const filters = [
    "Период",
    "Команда",
    "Должность",
    "Грейд",
    "Сотрудник",
    "Компетенция",
    "Навык",
  ];
  const selectedfilters = ["Core", "Медиа"];

  return (
    <section>
      <div className="filters">
        <FilterItem filter="Период" />
        {filters.map((filter) => (
          <FilterItem key={uuidv4()} filter={filter} />
        ))}
        <button className="filters__submit-button">Применить фильтры</button>
        <DownloadDashbord minimalism={false} />
      </div>
      <ul className="filters__marks">
        <li>
          <button className="filters__delete-all"></button>
        </li>
        {selectedfilters.map((item) => (
          <li className="filters__mark" key={uuidv4()}>
            <div className="filters__mark-span">{item}</div>
            <button className="filters__mark-del">
              <img src={delCross} />
            </button>
          </li>
        ))}
      </ul>
    </section>
  );
}

export default Filters;
