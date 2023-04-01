import EditIcon from "@mui/icons-material/Edit";

//icon edit button
const EditButton = ({ onClick }) => {
  return (
    <div>
      <button type="button" onClick={onClick}>
        <EditIcon className="group text-[#999999] hover:text-primary cursor-pointer" />
      </button>
    </div>
  );
};

export default EditButton;