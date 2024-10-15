import DonutChart from "./DonutChart/DonutChart";
import "./MainPage.scss";
import StaticCards from "./StaticCards/StaticCards";
import Compitents from "./Compitents/Compitents";
import RaitingDinamics from "./RaitingDinamics/RaitingDinamics.tsx";
import SkillsTable from "./SkillsTable/SkillsTable.tsx";

function MainPage() {
  const gradesData = [
    { name: "25% Junior", value: 25 },
    { name: "46% Middle", value: 46 },
    { name: "22% Senior", value: 22 },
  ];
  const gradesColors = ["#008E74", "#B342E8", "#08AEAE"];

  const skillsData = [
    { name: "15% Не владеет", value: 15 },
    { name: "31% Начальный", value: 31 },
    { name: "9% Базовый", value: 9 },
    { name: "19% Уверенный", value: 19 },
    { name: "20% Эксперт", value: 20 },
  ];
  const skillsColors = [
    "#E10D34",
    "#008E74",
    "#24E7E5",
    "#B342E8",
    "#08AEAE",
    "#221670",
  ];

  return (
    <main className="main">
      <section className="main__title-group">
        <h2 className="main__title">Аналитика навыков</h2>
        <span className="main__title-span">18 сотрудников</span>
      </section>
      <section className="analyst">
        <StaticCards />
        <DonutChart
          data={gradesData}
          colors={gradesColors}
          title="Распределение по грейдам"
        />
        <DonutChart
          data={skillsData}
          colors={skillsColors}
          title="Распределение по владению навыками"
        />
      </section>
      <section className="analyst">
        <Compitents />
        <RaitingDinamics />
      </section>
      <section className="table">
        <SkillsTable />
      </section>
    </main>
  );
}

export default MainPage;
