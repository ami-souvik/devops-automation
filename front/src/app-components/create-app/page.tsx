import { useState } from "react";
import { useNavigate } from "react-router";
import Layout from "@/layout"
import NewAppForm from "@/app-components/create-app/new-app-form"
import api from "@/lib/webservices"
import { useDispatch } from "react-redux";
import { setAz } from "@/slices/data-slice";

export default function Page() {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const [loading, setLoading] = useState(false);
  function onSubmit(data) {
    setLoading(true)
    api.post('/apps/create', data)
    setLoading(false)
    dispatch(setAz(data.availability_zone))
    navigate(`/apps/${data.app_name}`); 
  }
  return <Layout>
    <div className="flex flex-col place-items-center place-content-center space-y-2">
      <NewAppForm {...{loading, onSubmit}} />
    </div>
  </Layout>
}