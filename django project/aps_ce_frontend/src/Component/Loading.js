import React from "react";

export const Loading = () => {
  return (
    <div className="flex flex-col justify-center items-center">
      <div className="p-14 animate-pulse animate-text bg-[#FB8500] bg-clip-text text-transparent text-3xl font-semibold">
        กำลังโหลด ...
      </div>
      <div className="flex space-x-3">
        <div className="animate-bounce w-8 h-8 p-2 bg-[#5E000C] rounded-full" />
        <div className="animate-pulse hover:animate-ping w-8 h-8 p-2 bg-[#C1000F] rounded-full" />
        <div className="animate-bounce w-8 h-8 p-2 bg-[#F32D17] rounded-full" />
        <div className="animate-pulse w-8 h-8 p-2 bg-[#FD8839] rounded-full" />
      </div>
    </div>
  );
};