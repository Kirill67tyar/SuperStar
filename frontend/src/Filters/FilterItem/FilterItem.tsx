import React, { useState, useEffect, useRef } from "react";
import { v4 as uuidv4 } from "uuid";
import "./FilterItem.scss";
import arrowDown from "../../assets/icons/arrow-down.svg";
import arrowUp from "../../assets/icons/arrow-up.svg";

interface IFilterName {
  filter: string;
  filterMark?: string;
}

const FilterItem: React.FC<IFilterName> = ({ filter }) => {
  const itemsList = [
    "Дизайнер",
    "Девелопер",
    "Делопроизводитель",
    "Диспетчер",
    "Дизайнер",
    "Девелопер",
    "Делопроизводитель",
    "Диспетчер",
  ];
  const [filterListOpen, setFilterListOpen] = useState(false);
  const popupRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        popupRef.current &&
        !popupRef.current.contains(event.target as Node)
      ) {
        setFilterListOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [popupRef]);

  function handleFilterOpen() {
    setFilterListOpen(!filterListOpen);
  }

  return (
    <div ref={popupRef} className="filter-item">
      <button
        className={
          !filterListOpen
            ? "filter-item__button"
            : "filter-item__button filter-item__button_open"
        }
        onClick={handleFilterOpen}
      >
        {filter}
        <img
          className="filter-item__button-logo"
          src={!filterListOpen ? arrowDown : arrowUp}
        />
      </button>
      {
        <div
          ref={popupRef}
          className="filter-item__container"
          style={{ display: !filterListOpen ? "none" : "block" }}
        >
          <input
            className="filter-item__input"
            type="input"
            placeholder="Найти"
          />
          <ul className="filter-item__list">
            {itemsList.map((item) => (
              <li className="filter-item__list-item" key={uuidv4()}>
                <input className="filter-item__ckeckbox" type="checkbox" />
                <label className="filter-item__label">{item}</label>
              </li>
            ))}
          </ul>
        </div>
      }
    </div>
  );
};

export default FilterItem;
