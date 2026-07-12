import ManagementPage from '../components/pages/ManagementPage';
import { managementConfigs } from '../config/entityConfigs';

export default function Drivers() {
  return <ManagementPage config={managementConfigs.drivers} />;
}