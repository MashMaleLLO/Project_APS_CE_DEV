import AddIcon from "@mui/icons-material/Add";

//add icon button
const AddButton = ({ onClick }) => {
  return (
    <div>
      <button
        type="button"
        onClick={onClick}
        className="w-[120px] text-white font-bold text-sm md:text-base px-4 py-2 rounded-lg bg-[#FB8500] hover:bg-[#F28204] cursor-pointer"
      >
        <AddIcon className="text-white" />
        เพิ่มข้อมูล
      </button>
    </div>
  );
};

export default AddButton;