import "./TrainingPage.scss";
import { useEffect, useState } from "react";
import defaultPhoto from "../assets/images/photo-default.svg";

interface ITrainingData {
  id: number;
  employee: {
    name: string;
    position: string;
    grade: string;
    bus_factor: boolean;
  };
  skill: {
    competence: string;
    name: string;
    skill_course: string;
    time_of_training: string;
  };
  request_count: number;
}
[];

/* interface TrainingData {
    request_count: number,
    results: {
        cours: {
            name: string
            skill: {
                name: string,
                employees: {
                    name: string,
                    position: string,
                    grade: string,
                    bus_factor: boolean,
                    test_data: {
                        employee: number,
                        position: number,
                        grade: number
                    }
                }[]
            }[]
        }
    }
} */

function TrainingPage() {
  const item = {
    bus_factor: true,
    name: "Иванова Екатерина",
    position: "Дизайнер",
    grade: "Junior",
  };

  const [data, setData] = useState<ITrainingData[]>([]);
  console.log(data);

  useEffect(() => {
    fetch(`../../front.json`)
      .then((response) => response.json())
      .then((data) => {
        setData(data);
      })
      .catch((res) => {
        console.log("Ошибка при получении данных:", res.message);
      });
  }, []);

  return (
    <section className="training">
      <div className="training__header">
        <h2 className="main__title">Запросы на обучение</h2>
        <span className="main__title-span">26</span>
      </div>
      <div className="training__main">
        <table>
          <thead>
            <tr className="training__tr">
              <th className="training__competents">Компетенция</th>
              <th className="training__skill">Навык</th>
              <th className="training__program"> Обучающая программа</th>
              <th className="training__employer">Сотрудник</th>
            </tr>
          </thead>
          <tbody>
            <tr className="training__tr">
              <td className="training__courses">
                <p className="training__courses-name">
                  Навык работы с графическими редакторами
                </p>
              </td>
              <td className="training__courses">
                <p className="training__courses-name">Photoshop</p>
              </td>
              <td className="training__courses training__courses-cell">
                <p className="training__courses-name training__courses_item">
                  Photoshop для продолжающих
                </p>
                <p className="training__dates">15.10.24-25.11.24</p>
                <div className="training__employee-count">2</div>
              </td>
              <td className="training__employee-list">
                <div className="employee">
                  <img
                    className={
                      !item.bus_factor
                        ? "employee__image"
                        : "employee__image_true"
                    }
                    src={defaultPhoto}
                  />
                  <div>
                    <p className="employee__name">{item.name}</p>
                    <p className="employee__position">{`${item.position}, ${item.grade}`}</p>
                  </div>
                </div>
                <div className="employee">
                  <img
                    className={
                      !item.bus_factor
                        ? "employee__image"
                        : "employee__image_true"
                    }
                    src={defaultPhoto}
                  />
                  <div>
                    <p className="employee__name">{item.name}</p>
                    <p className="employee__position">{`${item.position}, ${item.grade}`}</p>
                  </div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  );
}

export default TrainingPage;
