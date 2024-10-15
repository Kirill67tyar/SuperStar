import { useState, useEffect } from "react";
import "./SkillsTable.scss";
import DownloadDashbord from "../../DownloadDashbord/DownloadDashbord";
import defaultPhoto from "../../assets/images/photo-default.svg";
import errowDown from "../../assets/icons/sort-arrow.svg";
import MyTooltip from "../../MyTooltip/MyTooltip";
import progressUp from "../../assets/icons/progress-arrow-up.svg";

interface ISkills {
  soft_skills: {
    accordance: boolean;
    grows: boolean;
    id: number;
    name: string;
    penultimate_score: number;
    score: number;
  }[];
  hard_skills: {
    accordance: boolean;
    grows: boolean;
    id: number;
    name: string;
    penultimate_score: number;
    score: number;
  }[];
}

interface IEmployer {
  bus_factor: boolean;
  created: number;
  grade: string;
  name: string;
  position: string;
  team: {
    name: string;
    id: number;
  }[];
  skills: ISkills;
}
[];

const teams = ["Core", "Mode"];

const SkillsTable = () => {
  const [hardSkills, setHardSkills] = useState<boolean>(true);
  const [currentTeam, setCurrentTeam] = useState<string>("");
  const [softSkillsList, setSoftSkillsList] = useState<string[]>([]);
  const [hardSkillsList, setHardSkillsList] = useState<string[]>([]);
  const [employers, setEmployers] = useState<IEmployer[]>([]);

  useEffect(() => {
    fetch(`../../../new_repsponse.json`)
      .then((response) => response.json())
      .then((data) => {
        setEmployers(data.employees);
        setCurrentTeam(data.current_team);
      })
      .catch((res) => {
        console.log("Ошибка при получении данных:", res.message);
      });
  }, []);

  if (!employers) {
    return <p>Загрузка данных...</p>;
  }
  useEffect(() => {
    const softList = Array.from(
      new Set(
        employers.flatMap((item) =>
          item.skills?.soft_skills?.map((item) => item.name),
        ),
      ),
    );
    setSoftSkillsList(softList);
    const hardList = Array.from(
      new Set(
        employers.flatMap((item) =>
          item.skills?.hard_skills?.map((item) => item.name),
        ),
      ),
    );
    setHardSkillsList(hardList);
  }, [employers]);
  function handleSoftSkills() {
    setHardSkills(false);
  }
  function handleHardSkills() {
    setHardSkills(true);
  }
  function handleTeam(team: string) {
    setCurrentTeam(team);
  }

  const [showTooltip, setShowTooltip] = useState<string | null>(null); // Состояние для отслеживания индекса видимого тултипа

  const handleMouseOver = (index: string) => {
    setShowTooltip(index); // Устанавливаем индекс видимого тултипа
  };

  const handleMouseOut = () => {
    setShowTooltip(null); // Скрываем тултип при выходе мыши
  };

  const handleSort = (skill: string) => {
    console.log("здесь могла бы быть сортировка по", { skill });
  };

  /*
    const [sortBy, setSortBy] = useState(''); // Store the column to sort by
    const [sortedData, setSortedData] = useState<IEmployer[]>([])
  
  
   
      
  
  */

  return (
    <>
      <div className="skills__header">
        <div className="skills__download">
          <DownloadDashbord minimalism={true} />
        </div>
        <h2 className="skills__title">Средняя экспертная оценка навыков</h2>
        <div className="skills__buttons">
          <button
            className={`skills__skills-button ${hardSkills ? "skills__skills-button_active" : ""}`}
            onClick={handleHardSkills}
          >
            Hard skills
          </button>
          <button
            className={`skills__skills-button  ${!hardSkills ? "skills__skills-button_active" : ""}`}
            onClick={handleSoftSkills}
          >
            Soft skills
          </button>
        </div>
        <div className="skills__buttons skills__buttons-teams">
          {teams.map((team) => (
            <button
              className={`skills__skills-button ${currentTeam == team ? "skills__skills-button_active" : ""}`}
              onClick={() => {
                handleTeam(team);
              }}
            >
              {team}
            </button>
          ))}
        </div>
      </div>

      <div className="table__container">
        <div className="table__team">
          <h4 className="table__header">Команда</h4>
          <p className="table__team-name">{currentTeam}</p>
        </div>
        <div className="table__main"></div>
        <table>
          <thead>
            <tr>
              <th className="table__employeer">
                Сотрудник
                <button
                  className="table__sort-button"
                  onMouseOver={() => handleMouseOver("159")}
                  onMouseOut={handleMouseOut}
                  onClick={() => handleSort("Сотрудник")}
                ></button>
                <MyTooltip
                  showTooltip={showTooltip === "159"}
                  text="Сортировка"
                />
              </th>
              <th className="table__raiting">
                Рейтинг
                <button
                  className="table__sort-button"
                  onMouseOver={() => handleMouseOver("147")}
                  onMouseOut={handleMouseOut}
                  onClick={() => handleSort("Рейтинг")}
                ></button>
                <MyTooltip
                  showTooltip={showTooltip === "147"}
                  text="Сортировка"
                />
              </th>
              {hardSkills &&
                hardSkillsList.map((skillName, index) => (
                  <th key={index} className="table__skill">
                    <div className="table__skill-container">
                      <p className="table__skill-text">{skillName}</p>
                      <button
                        className="table__sort-button"
                        onMouseOver={() => handleMouseOver(String(index))}
                        onMouseOut={handleMouseOut}
                        onClick={() => handleSort(skillName)}
                      ></button>
                      <MyTooltip
                        showTooltip={showTooltip === String(index)}
                        text="Сортировка"
                      />
                    </div>
                  </th>
                ))}
              {!hardSkills &&
                softSkillsList.map((skillName, index) => (
                  <th key={index} className="table__skill">
                    <p>{skillName}</p>
                    <button
                      className="table__sort-button"
                      onMouseOver={() => handleMouseOver(String(index))}
                      onMouseOut={handleMouseOut}
                      onClick={() => handleSort(skillName)}
                    >
                      <img src={errowDown} alt="sort Icon" />
                    </button>
                    <MyTooltip
                      showTooltip={showTooltip === String(index)}
                      text="Сортировка"
                    />
                  </th>
                ))}
            </tr>
          </thead>

          <tbody>
            {employers.map((item, index) => (
              <tr className="table__row" key={index}>
                <td className="employee">
                  <div>{index + 1}</div>
                  <img
                    className={
                      !item.bus_factor
                        ? "employee__image"
                        : "employee__image_true"
                    }
                    src={defaultPhoto}
                    onMouseOver={() => handleMouseOver(index + "bus-factor")}
                    onMouseOut={handleMouseOut}
                  />
                  {item.bus_factor && (
                    <MyTooltip
                      showTooltip={showTooltip === String(index + "bus-factor")}
                      text={"Bus Factor"}
                    />
                  )}
                  <div>
                    <p className="employee__name">{item.name}</p>
                    <p className="employee__position">{`${item.position}, ${item.grade}`}</p>
                  </div>
                </td>
                <td>
                  <div className="employee__raiting">99/100</div>
                </td>
                {hardSkills &&
                  item.skills.hard_skills.map((i) => (
                    <td>
                      <div className="employee__score">
                        <img
                          className="employee__score-progress"
                          src={progressUp}
                          alt="прогресс"
                        />
                        <p className="employee__score-value">{i.score}</p>
                      </div>
                    </td>
                  ))}
                {!hardSkills &&
                  item.skills.soft_skills.map((i) => (
                    <td className="employe__score">
                      <img className="employe__score-progress" />
                      <p className="employe__score-value">{i.score}</p>
                    </td>
                  ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
};

export default SkillsTable;
