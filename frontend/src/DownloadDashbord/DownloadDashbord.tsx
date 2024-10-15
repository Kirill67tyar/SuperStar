import "./DownloadDashbord.scss";
import { useState, useEffect, useRef } from "react";

interface IProps {
  minimalism?: boolean;
}

const DownloadDashbord: React.FC<IProps> = ({ minimalism }) => {
  const [filterListOpen, setFilterListOpen] = useState(false);
  const dashbordRef = useRef<HTMLDivElement>(null);
  const [selectedItems, setSelectedItems] = useState<string[]>([]);

  /* const downloadPdf = () => {
         const element = document.body.innerHTML;
         const opt = {
             margin: 10,
             filename: 'Factuur <?php echo $factuurnaam ?>.pdf',
             image: { type: 'jpeg', quality: 1 },
             html2canvas: { letterRendering: false, width: 1440, height: 1920 },
             jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' },
             pagebreak: { mode: ['avoid-all', 'css'] }
         };
         // Choose the element and save the PDF for our user.
         html2pdf().from(element).set(opt).save();
         document.body.innerHTML = element;
 
     };
     
     const downloadJpeg = () => {
         const element = document.getElementById('root');
         html2canvas(element).then(canvas => {
             const link = document.createElement('root');
             link.download = 'my-page.jpeg';
             link.href = canvas.toDataURL('image/jpeg');
             link.click();
         });
     }; */

  const downloadExcel = () => {
    console.log("функционал в разработке");
  };

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        dashbordRef.current &&
        !dashbordRef.current.contains(event.target as Node)
      ) {
        setFilterListOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  function handleFilterOpen() {
    setFilterListOpen(!filterListOpen);
  }

  const handleCheckboxChange = (itemId: string) => {
    if (selectedItems.includes(itemId)) {
      setSelectedItems(selectedItems.filter((id) => id !== itemId));
    } else {
      setSelectedItems([...selectedItems, itemId]);
    }
  };

  function handleSubmit() {
    if (selectedItems.includes("pdf")) {
      console.log("pdf");
    } else if (selectedItems.includes("excel")) {
      downloadExcel();
    }
    setFilterListOpen(false);
  }

  return (
    <div ref={dashbordRef} className="download-dashbord">
      {!minimalism ? (
        <button
          className="download-dashbord__button"
          onClick={handleFilterOpen}
        >
          <div
            className={
              !filterListOpen
                ? "download-dashbord__button-img"
                : "download-dashbord__button-img box-shadow"
            }
          ></div>
          <span
            className={
              !filterListOpen
                ? "download-dashbord__button-span"
                : "download-dashbord__button-span box-shadow"
            }
          >
            Скачать план
          </span>
        </button>
      ) : (
        <button
          className={
            !filterListOpen
              ? "download-dashbord__mini-button"
              : "download-dashbord__mini-button box-shadow"
          }
          onClick={handleFilterOpen}
        ></button>
      )}
      {filterListOpen && (
        <div className="download-dashbord__container">
          <p className="download-dashbord__text">
            Выберите формат для скачивания
          </p>
          <ul className="download-dashbord__list">
            <li className="download-dashbord__list-item">
              <input
                className="download-dashbord__ckeckbox"
                type="checkbox"
                id="excel"
                checked={selectedItems.includes("excel")}
                onChange={() => handleCheckboxChange("excel")}
              />
              <label htmlFor="excel" className="download-dashbord__label">
                Excel
              </label>
            </li>
            <li className="download-dashbord__list-item">
              <input
                id="pdf"
                className="download-dashbord__ckeckbox"
                type="checkbox"
                checked={selectedItems.includes("pdf")}
                onChange={() => handleCheckboxChange("pdf")}
              />
              <label htmlFor="pdf" className="download-dashbord__label">
                PDF
              </label>
            </li>
            <li className="download-dashbord__list-item">
              <input
                id="jpeg"
                className="download-dashbord__ckeckbox"
                type="checkbox"
                checked={selectedItems.includes("jpeg")}
                onChange={() => handleCheckboxChange("jpeg")}
              />
              <label htmlFor="jpeg" className="download-dashbord__label">
                JPEG
              </label>
            </li>
          </ul>
          <button
            className="download-dashbord__submit-button"
            onClick={handleSubmit}
          >
            Скачать
          </button>
        </div>
      )}
    </div>
  );
};

export default DownloadDashbord;
