"use client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Search } from "lucide-react";
import React from "react";
import { useState } from "react";

const SearchBar = () => {
  // States for form fields
  const [street, setStreet] = useState("");
  const [city, setCity] = useState("");
  const [state, setState] = useState("");
  const [zipCode, setZipCode] = useState("");
  const [radius, setRadius] = useState("");
  const [condition, setCondition] = useState("");
  const [insurance, setInsurance] = useState<string | undefined>(undefined);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault(); // Prevent form from refreshing the page

    try {
      const response = await fetch("http://localhost:5000/api/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          street,
          city,
          state,
          zip_code: zipCode,
          condition,
          insurance,
        }),
      });

      const data = await response.json();
      console.log("Search Results:", data);
    } catch (error) {
      console.error("Error during fetch:", error);
    }
  };

  return (
    <div className="w-full space-y-2 max-w-xl">
      <form
        className="flex flex-col space-y-2 sm:flex-row sm:space-x-2 sm:space-y-0 items-center justify-center"
        onSubmit={handleSubmit}
      >
        <div className="flex flex-col space-y-2">
          <Input
            className="max-w-lg flex-1 bg-white p-2"
            placeholder="Street Address"
            type="text"
            value={street} // Bind to street state
            onChange={(e) => setStreet(e.target.value)} // Update street state on input change
          />
          <Input
            className="max-w-lg flex-1 bg-white p-2"
            placeholder="City"
            type="text"
            value={city} // Bind to city state
            onChange={(e) => setCity(e.target.value)} // Update city state on input change
          />
          <Input
            className="max-w-lg flex-1 bg-white p-2"
            placeholder="State"
            type="text"
            value={state} // Bind to state state
            onChange={(e) => setState(e.target.value)} // Update state state on input change
          />
          <Input
            className="max-w-lg flex-1 bg-white p-2"
            placeholder="Zip Code"
            type="text"
            value={zipCode} // Bind to zip code state
            onChange={(e) => setZipCode(e.target.value)} // Update zip code state on input change
          />
          <Input
            className="max-w-lg flex-1 bg-white p-2"
            placeholder="Radius"
            type="text"
            value={radius} // Bind to radius state
            onChange={(e) => setRadius(e.target.value)} // Update radius state on input change
          />
          <Input
            className="max-w-lg flex-1 bg-white p-2"
            placeholder="Medical Condition"
            type="text"
            value={condition} // Bind to condition state
            onChange={(e) => setCondition(e.target.value)} // Update condition state on input change
          />
        </div>
        <div className="flex flex-col space-y-2">
          <Select
            onValueChange={(value) => setInsurance(value)} // Update insurance state on selection change
          >
            <SelectTrigger className="bg-white text-gray-700 p-2">
              <SelectValue placeholder="Insurance" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="medicare">Medicare</SelectItem>
              <SelectItem value="medicaid">Medicaid</SelectItem>
              <SelectItem value="private">Private Insurance</SelectItem>
              <SelectItem value="uninsured">Uninsured</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <Button
          type="submit"
          className="bg-white text-primary hover:bg-white/90 h-full"
        >
          <Search className="" />
        </Button>
      </form>
    </div>
  );
};

export default SearchBar;
