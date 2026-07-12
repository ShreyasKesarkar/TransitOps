import ManagementPage from '../components/pages/ManagementPage';
import { managementConfigs } from '../config/entityConfigs';

export default function Trips() {
  return <ManagementPage config={managementConfigs.trips} />;
}